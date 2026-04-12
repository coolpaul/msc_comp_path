from pydicom import dcmread
import pylab
# python3.12 -m pip install pillow # this package needs to be installed
# python3.12 -m pip install python-gdcm # this package needs to be installed

def show_dicom(file_name, map='gray_r'):
        # cmap could be 'gray' (grayscale), 'gray_r' (reverse grayscale), pylab.cm.bone
        ds = dcmread(file_name)

        # show metadata
        for element in ds:
                print(element)

        rows = ds.Rows
        cols = ds.Columns
        print(f"Image Dimensions: {rows} x {cols} pixels")

        # access specific data (ie study date: (0008,0020)
        study_date_time = f'{ds.StudyDate}_{ds.StudyTime}'
        study_description = ds.StudyDescription
        patient_dob = ds.PatientBirthDate
        patient_age = ds.PatientAge
        patient_gender = ds.PatientSex
        print(f'The study date and time is {study_date_time}')
        print(f'The study is: {study_description}')
        print(f'The patient was born on {patient_dob}, is {patient_age} years old and the gender is {patient_gender}')
        pylab.imshow(ds.pixel_array, cmap=map) 
        pylab.show()
        return

if __name__ == '__main__':  
        image_path = '../data/xray/00000001' 
        show_dicom(image_path, map='gray_r')
        show_dicom(image_path, map='gray')


