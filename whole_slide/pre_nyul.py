# -*-coding:utf-8-*-
from dipy.io.image import load_nifti, save_nifti
from dipy.denoise.nlmeans import nlmeans
from dipy.denoise.noise_estimate import estimate_sigma
import SimpleITK as sitk
import numpy as np
import nibabel as nib
from nilearn.image import resample_img

'''
e.g. 
image_path='/root/mri/raw/image/demo_image.nii'
mask_path='/root/mri/raw/image/demo_image.nrrd'
save_image_path='/root/mri/preprocess/image/demo_image.nii'
save_mask_path='/root/mri/preprocess/image/demo_image.nrrd'

'''


def process(image_path, mask_path, save_image_path, save_mask_path):
    # denise image
    data, affine = load_nifti(image_path)
    sigma = estimate_sigma(data)
    den = nlmeans(data, sigma)
    save_nifti('temp_image.nii', den, affine)

    # N4 bias field correction
    image_file = sitk.ReadImage('temp_image.nii', sitk.sitkFloat32)
    mask_file = sitk.ReadImage(mask_path, sitk.sitkUInt8)
    
    # in case you are using 3D data or doing the registration
    if image_file.GetDirection() != (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
        image_file.SetDirection((1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))

    # without this, might cause errors in some files
    mask_file.SetOrigin(image_file.GetOrigin())
    mask_file.SetSpacing(image_file.GetSpacing())
    mask_file.SetDirection(image_file.GetDirection())

    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    correct_image = corrector.Execute(image_file, mask_file)

    sitk.WriteImage(correct_image, 'temp_image.nii')
    sitk.WriteImage(mask_file, 'temp_mask.nii')

    # resampling
    temp_file = nib.load('temp_image.nii')
    new_file = resample_img(temp_file, target_affine=np.eye(3), interpolation='nearest')
    nib.save(new_file, save_image_path)

    mask_file = nib.load('temp_mask.nii')
    new_file = resample_img(mask_file, target_affine=np.eye(3), interpolation='nearest')
    nib.save(new_file, save_mask_path)


process(image_path='BH_Ax_LAVA+C_4_0_2_axial_PV.nii',
        mask_path='BH_Ax_LAVA+C_4_0_2_axial_PV.nrrd',
        save_image_path='image.nii',
        save_mask_path='mask.nrrd')
