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

    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    correct_image = corrector.Execute(image_file, mask_file)

    sitk.WriteImage(correct_image, 'temp_image.nii')
    sitk.WriteImage(mask_file, 'temp_mask.nii')

    # resampling
    temp_file = nib.load('temp_image.nii')
    new_file = resample_img(temp_file, target_affine=np.eye(3), interpolation='nearest')
    nib.save(new_file, 're_image.nii')

    mask_file = nib.load('temp_mask.nii')
    new_file = resample_img(mask_file, target_affine=np.eye(3), interpolation='nearest')
    nib.save(new_file, 're_mask.nii')

    # normalization
    image = sitk.ReadImage('re_image.nii', sitk.sitkFloat32)
    mask = sitk.ReadImage('re_mask.nii', sitk.sitkUInt8)

    image_array = sitk.GetArrayFromImage(image)

    mean_value = np.mean(image_array)
    std_value = np.std(image_array)
    new_image_array = (image_array - mean_value) / std_value

    new_image = sitk.GetImageFromArray(new_image_array,
                                       isVector=image.GetNumberOfComponentsPerPixel() > 1)
    new_image.SetOrigin(image.GetOrigin())
    new_image.SetSpacing(image.GetSpacing())
    new_image.SetDirection(image.GetDirection())

    sitk.WriteImage(new_image, save_image_path)
    sitk.WriteImage(mask, save_mask_path)


process(image_path='1148333_4322223_BH_Ax_LAVA+C_4_0_2_axial_PV.nii',
        mask_path='1148333_4322223_BH_Ax_LAVA+C_4_0_2_axial_PV.nrrd',
        save_image_path='image.nii',
        save_mask_path='mask.nrrd')
