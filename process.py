# -*-coding:utf-8-*-
from dipy.io.image import load_nifti, save_nifti
from dipy.denoise.nlmeans import nlmeans
from dipy.denoise.noise_estimate import estimate_sigma
import os

import SimpleITK as sitk

import numpy as np
import os
import nibabel as nib
from nilearn.image import resample_img

'''
在预处理前，需要注意到的，mask数组里面只能存在0或者1这两种值，不然在bias field correction阶段会出问题
主要是以下几个步骤：
1.denoise
2.bias field correction
3.resample
4.z-score
输出的就是预处理之后的图像(nii格式)和mask（nrrd格式）
'''

'''
这里只需要输入image就可以
'''
def denoise_mri(root_path, save_path):
    phase_name_list = ['pv', 'art', 't2', 'dwi1']
    for stage in ['test', 'train']:
        for fold_mark in ['image']:
            for pn in phase_name_list:
                filenames = os.listdir(root_path + pn + '/'+stage+'/'+fold_mark+'/')
                for fn in filenames:
                    data, affine = load_nifti(root_path + pn + '/'+stage+'/'+fold_mark+'/'+fn)
                    sigma = estimate_sigma(data)

                    den = nlmeans(data, sigma)
                    save_dir = save_path+ pn + '/'+stage+'/'+fold_mark+'/'
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    save_nifti(save_dir+fn, den, affine)


'''
这里需要输入image和对应的mask
'''
def N4_bias_field_correction_tumor_mask(image_path, mask_path, save_image_path, save_mask_path):

    image_file = sitk.ReadImage(image_path, sitk.sitkFloat32)
    mask_file = sitk.ReadImage(mask_path, sitk.sitkUInt8)

    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    correct_image = corrector.Execute(image_file, mask_file)
    sitk.WriteImage(correct_image, save_image_path)
    sitk.WriteImage(mask_file, save_mask_path)


'''
这里的处理对mask文件有改动
'''
def resample_mri(image_path, save_image_path, mask_path, save_mask_path):
    temp_file = nib.load(image_path)
    new_file = resample_img(temp_file, target_affine=np.eye(3), interpolation='linear')
    nib.save(new_file, save_image_path)

    temp_file = nib.load(mask_path)
    new_file = resample_img(temp_file, target_affine=np.eye(3), interpolation='linear')
    nib.save(new_file, save_mask_path)


'''
对整个volume进行的z_score
'''
def zscore_volume(image_path, mask_path, save_image_path, save_mask_path):
    image = sitk.ReadImage(image_path, sitk.sitkFloat32)
    mask = sitk.ReadImage(mask_path, sitk.sitkUInt8)

    image_array = sitk.GetArrayFromImage(image)
    mask_array = sitk.GetArrayFromImage(mask)

    mean_value = np.mean(image_array)
    std_value = np.std(image_array)
    new_image_array = (image_array - mean_value) / std_value

    np.save(save_image_path, new_image_array)
    np.save(save_mask_path, mask_array)