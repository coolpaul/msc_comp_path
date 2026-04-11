# python openslide environment

import os
import sys
import openslide
import numpy as np

# read svs file with openslide
def read_svs_file_divide_patches(svs_file=None, patch_size=None, level=0, min_pixel_value=150, max_pixel_value=230, output_dir=None):
    '''
    Read svs file and divide into patches
    :param svs_file: path to svs file
    :param patch_size: size of patches (width, height)
    :param output_dir: directory to save patches
    :param level: level of svs file to read (0 is the highest resolution)
    :param min_pixel_value: minimum pixel value to save patch (0-255); lower is darker
    :param max_pixel_value: maximum pixel value to save patch (0-255); higher is lighter
    :return: None
    '''
    # check if file exists
    if not os.path.isfile(svs_file):
        print(f"File {svs_file} does not exist.")
        sys.exit(1)
    
    # extract filename from path and remove file extension
    file_name = os.path.basename(svs_file)
    file_name = os.path.splitext(file_name)[0]

    # read svs file
    slide = openslide.OpenSlide(svs_file)
    slide_dimensions = slide.dimensions
    print(f"Slide dimensions: {slide_dimensions}")

    # calculate number of patches
    num_patches_x = int(slide_dimensions[0] / patch_size[0])
    num_patches_y = int(slide_dimensions[1] / patch_size[1])

    # create patches
    for i in range(num_patches_x):
        for j in range(num_patches_y):
            x = i * patch_size[0]
            y = j * patch_size[1]
            patch = slide.read_region(location=(x, y), size=patch_size, level=level)
            mean = np.array(patch).mean()
            if mean >= min_pixel_value and mean <= max_pixel_value:
                patch = patch.convert("RGB") # convert patch to jpeg format
                patch.save(os.path.join(output_dir, f"{file_name}_{x}_{y}.jpg"))
    return 


if __name__ == "__main__":

    input_dir = "../data/wsi/"
    output_dir = "../data/patches/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # set patch size
    patch_size = (512, 512) 

    # list svs files in the desktop directory
    svs_files = os.listdir(input_dir)

    # loop through svs files
    for svs_file in svs_files:
        # check if file is a svs file
        if not svs_file.endswith(".svs"):
            continue
        full_path = os.path.join(input_dir, svs_file)
        print(full_path)
        # read svs file and divide into patches    
        read_svs_file_divide_patches(svs_file=svs_file, 
                                     patch_size=patch_size, 
                                     level=0, 
                                     min_pixel_value=160, 
                                     max_pixel_value=230, 
                                     output_dir=output_dir)

    

