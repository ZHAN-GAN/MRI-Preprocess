# -*-coding:utf-8-*-
import os
from whole_slide.nyul_tool import *
import shutil
import SimpleITK as sitk


'''
We need to fit all the training MRI into the nyul algorithm to train a optimal template, 
and then, we can fit the training MRI and testing MRI to the trained template to obtain 
the standard training MRI and standard testing MRI.
'''

def nyul_image(root_path, save_nyul_path):
    # for 5-fold cross validation setting.
    for i in range(5):
        phase_name_list = ['pv', 'art', 'dwi1', 't2']
        # train the template for each phase using the training data
        for pn in phase_name_list:
            temp_train_path = root_path + str(i) + '/' + pn +'/train/image/'
            train_filenames = os.listdir(temp_train_path)
            print('training samples: '+str(len(train_filenames)))
            train_list = []
            for fn in train_filenames:
                temp_key = temp_train_path+fn
                train_list.append(temp_key)

            standard_scale, perc = nyul_train_standard_scale(train_list)
            standard_path = str(i) + '_' +pn + '.npy'
            np.save(standard_path, [standard_scale, perc])

            save_dir = save_nyul_path + str(i) + '/' + pn + '/train/image/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            print('save')
            # obtain the standard training MRI
            for fn in train_filenames:
                raw_image = nib.load(temp_train_path+fn)
                print(temp_train_path+fn)
                save_temp_image = nyul_apply_standard_scale(raw_image.get_data(), str(i) + '_' +pn + '.npy')
                nib_image = nib.Nifti1Image(save_temp_image, raw_image.affine, raw_image.header)
                nib.save(nib_image, save_dir + fn)

            # obtain the standard testing MRI
            temp_test_path = root_path + str(i) + '/' + pn +'/test/image/'
            test_save_path = save_nyul_path + str(i) + '/' + pn + '/test/image/'
            if not os.path.exists(test_save_path):
                os.makedirs(test_save_path)
            test_filenames = os.listdir(temp_test_path)
            for fn in test_filenames:
                raw_image = nib.load(temp_test_path+fn)
                print(temp_test_path+fn)
                save_temp_test_image = nyul_apply_standard_scale(raw_image.get_data(), str(i) + '_' +pn + '.npy')
                nib_image = nib.Nifti1Image(save_temp_test_image, raw_image.affine, raw_image.header)
                nib.save(nib_image, test_save_path + fn)


def copy_mask(root_path, save_nyul_path):
    for i in range(5):
        phase_name_list = ['pv', 'art', 'dwi1', 't2']
        for pn in phase_name_list:
            mask_file_path = root_path + str(i) + '/' + pn +'/train/mask/'
            save_mask_path = save_nyul_path + str(i) + '/' + pn +'/train/mask/'
            if not os.path.exists(save_mask_path):
                os.makedirs(save_mask_path)
            mask_filenames = os.listdir(mask_file_path)
            for fn in mask_filenames:
                shutil.copyfile(src=mask_file_path + fn,
                                dst=save_mask_path + fn)


            mask_file_path = root_path + str(i) + '/' + pn +'/test/mask/'
            save_mask_path = save_nyul_path + str(i) + '/' + pn + '/test/mask/'
            if not os.path.exists(save_mask_path):
                os.makedirs(save_mask_path)
            mask_filenames = os.listdir(mask_file_path)
            for fn in mask_filenames:
                shutil.copyfile(src=mask_file_path + fn,
                                dst=save_mask_path + fn)


# z-score normalization
def normalization(save_nyul_path, save_norm_path):
    for i in range(5):
        phase_name_list = ['pv', 'art', 'dwi1', 't2']
        for pn in phase_name_list:
            temp_train_image_path = save_nyul_path + str(i) + '/' + pn + '/train/image/'
            temp_train_mask_path = save_nyul_path + str(i) + '/' + pn + '/train/mask/'
            train_filenames = os.listdir(temp_train_image_path)
            for fn in train_filenames:
                image = sitk.ReadImage(temp_train_image_path+fn, sitk.sitkFloat32)
                mask = sitk.ReadImage(temp_train_mask_path+fn, sitk.sitkUInt8)

                image_array = sitk.GetArrayFromImage(image)

                mean_value = np.mean(image_array)
                std_value = np.std(image_array)
                new_image_array = (image_array - mean_value) / std_value

                new_image = sitk.GetImageFromArray(new_image_array,
                                                   isVector=image.GetNumberOfComponentsPerPixel() > 1)
                new_image.SetOrigin(image.GetOrigin())
                new_image.SetSpacing(image.GetSpacing())
                new_image.SetDirection(image.GetDirection())

                fold_save_norm_image_path = save_norm_path + str(i) + '/' + pn + '/train/image/'
                if not os.path.exists(fold_save_norm_image_path):
                    os.makedirs(fold_save_norm_image_path)

                fold_save_norm_mask_path = save_norm_path + str(i) + '/' + pn + '/train/mask/'
                if not os.path.exists(fold_save_norm_mask_path):
                    os.makedirs(fold_save_norm_mask_path)

                sitk.WriteImage(new_image, fold_save_norm_image_path+fn)
                sitk.WriteImage(mask, fold_save_norm_mask_path+fn)

            # test
            temp_test_image_path = save_nyul_path + str(i) + '/' + pn + '/test/image/'
            temp_test_mask_path = save_nyul_path + str(i) + '/' + pn + '/test/mask/'
            test_filenames = os.listdir(temp_test_image_path)
            for fn in test_filenames:
                image = sitk.ReadImage(temp_test_image_path + fn, sitk.sitkFloat32)
                mask = sitk.ReadImage(temp_test_mask_path + fn, sitk.sitkUInt8)

                image_array = sitk.GetArrayFromImage(image)

                mean_value = np.mean(image_array)
                std_value = np.std(image_array)
                new_image_array = (image_array - mean_value) / std_value

                new_image = sitk.GetImageFromArray(new_image_array,
                                                   isVector=image.GetNumberOfComponentsPerPixel() > 1)
                new_image.SetOrigin(image.GetOrigin())
                new_image.SetSpacing(image.GetSpacing())
                new_image.SetDirection(image.GetDirection())

                fold_save_norm_image_path = save_norm_path + str(i) + '/' + pn + '/test/image/'
                if not os.path.exists(fold_save_norm_image_path):
                    os.makedirs(fold_save_norm_image_path)

                fold_save_norm_mask_path = save_norm_path + str(i) + '/' + pn + '/test/mask/'
                if not os.path.exists(fold_save_norm_mask_path):
                    os.makedirs(fold_save_norm_mask_path)

                sitk.WriteImage(new_image, fold_save_norm_image_path + fn)
                sitk.WriteImage(mask, fold_save_norm_mask_path + fn)

if __name__ == '__main__':

    nyul_image(root_path='/media/My Passport/HCC/cross/', save_nyul_path ='/media/My Passport/HCC/nyul_cross/')
    copy_mask(root_path='/media/My Passport/HCC/cross/', save_nyul_path ='/media/My Passport/HCC/nyul_cross/')
    normalization(save_nyul_path='/media/My Passport/HCC/nyul_cross/',
                  save_norm_path='/media/My Passport/HCC/nyul_norm/')

