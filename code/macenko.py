import numpy as np

# ==========================================
# 1. Reconstructed 'stain_utils' Functions
# ==========================================

def RGB_to_OD(I):
    """Converts RGB image to Optical Density (OD) space."""
    # Prevent divide-by-zero by ensuring minimum pixel value is 1
    I = np.maximum(I, 1) 
    return -np.log10(I / 255.0)

def OD_to_RGB(OD):
    """Converts Optical Density (OD) back to RGB."""
    return (255.0 * 10 ** (-OD)).astype(np.uint8)

def normalize_rows(A):
    """Normalizes the rows of an array."""
    return A / np.linalg.norm(A, axis=1)[:, None]

def standardize_brightness(I):
    """Standardizes brightness (Placeholder pass-through for Macenko)."""
    # Standard Macenko math usually handles intensity via OD conversion.
    # We clip to ensure valid RGB bounds.
    return np.clip(I, 0, 255)

def get_concentrations(I, stain_matrix):
    """Replaces the SPAMS lasso solver with standard NumPy least-squares."""
    OD = RGB_to_OD(I).reshape((-1, 3))
    # Solve for Concentrations (C): OD = C * stain_matrix
    C = np.linalg.lstsq(stain_matrix.T, OD.T, rcond=None)[0].T
    return C

# ==========================================
# 2. Provided Macenko Algorithm
# https://github.com/m4ln/stain-normalization-reinhard-macenko-vahadane/blob/main/models/stainNorm_Macenko.py
# ==========================================

def get_stain_matrix(I, beta=0.15, alpha=1):
    """
    Get stain matrix (2x3)
    :param I: Image array
    :param beta: OD threshold for background removal
    :param alpha: Tolerance for angular extremes
    """
    OD = RGB_to_OD(I).reshape((-1, 3))
    OD = (OD[(OD > beta).any(axis=1), :])
    
    if len(OD) == 0:
        raise ValueError("No tissue found in patch. Background threshold (beta) may be too high.")
        
    _, V = np.linalg.eigh(np.cov(OD, rowvar=False))
    V = V[:, [2, 1]]
    if V[0, 0] < 0: V[:, 0] *= -1
    if V[0, 1] < 0: V[:, 1] *= -1
    That = np.dot(OD, V)
    phi = np.arctan2(That[:, 1], That[:, 0])
    minPhi = np.percentile(phi, alpha)
    maxPhi = np.percentile(phi, 100 - alpha)
    v1 = np.dot(V, np.array([np.cos(minPhi), np.sin(minPhi)]))
    v2 = np.dot(V, np.array([np.cos(maxPhi), np.sin(maxPhi)]))
    
    if v1[0] > v2[0]:
        HE = np.array([v1, v2])
    else:
        HE = np.array([v2, v1])
        
    return normalize_rows(HE)


class Normalizer(object):
    """
    A stain normalization object (Modified to include default reference values)
    """
    def __init__(self):
        # Default ideal H&E stain vectors derived from pathology literature
        self.stain_matrix_target = np.array([
            [0.5626, 0.7201, 0.4062],  # Hematoxylin (Deep Purple/Blue)
            [0.2159, 0.8012, 0.5581]   # Eosin (Pink)
        ])
        # We manually normalize the rows of our hardcoded default matrix
        self.stain_matrix_target = normalize_rows(self.stain_matrix_target)
        
        self.target_concentrations = None
        # Standard maximum concentrations if no reference image is fitted
        self.maxC_target_default = np.array([[1.9705, 1.0308]])

    def fit(self, target):
        target = standardize_brightness(target)
        self.stain_matrix_target = get_stain_matrix(target)
        self.target_concentrations = get_concentrations(target, self.stain_matrix_target)

    def target_stains(self):
        return OD_to_RGB(self.stain_matrix_target)

    def transform(self, I):
        I = standardize_brightness(I)
        stain_matrix_source = get_stain_matrix(I)
        source_concentrations = get_concentrations(I, stain_matrix_source)
        
        maxC_source = np.percentile(source_concentrations, 99, axis=0).reshape((1, 2))
        
        # Use fitted concentrations if available, otherwise use defaults
        if self.target_concentrations is not None:
            maxC_target = np.percentile(self.target_concentrations, 99, axis=0).reshape((1, 2))
        else:
            maxC_target = self.maxC_target_default
            
        source_concentrations *= (maxC_target / maxC_source)
        
        # Reconstruct the image
        reconstructed_OD = np.dot(source_concentrations, self.stain_matrix_target).reshape(I.shape)
        # Convert back from OD space to RGB
        return (255 * np.exp(-1 * reconstructed_OD)).astype(np.uint8)

    def hematoxylin(self, I):
        I = standardize_brightness(I)
        h, w, c = I.shape
        stain_matrix_source = get_stain_matrix(I)
        source_concentrations = get_concentrations(I, stain_matrix_source)
        H = source_concentrations[:, 0].reshape(h, w)
        H = np.exp(-1 * H)
        return H
