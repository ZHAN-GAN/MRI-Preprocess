# MRI-Preprocess

## Pipeline:
This is a MRI preprocessing pipeline for deep learning, which mainly took advices from [chapter 5](https://www.researchgate.net/publication/309640957_MRI_preprocessing) in Imaging Biomarkers.

It contains 5 steps:
1. Denoise, we use the [Non-Local Means algorithm](https://dipy.org/documentation/1.5.0/examples_built/denoise_nlmeans/#example-denoise-nlmeans) to remove the noise from images.
2. Bias field correction, we use [N4 algorithm](https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html) to correcting low frequency intensity non-uniformity present in MRI image data.
3. Resampling, we use the method described in this [blog](https://www.kaggle.com/code/mechaman/resizing-reshaping-and-resampling-nifti-files/notebook) to make voxel spcaing the same across samples, such that we could extract generalized features in the feature extraction stage.
4. Standardlization, we use [nyul histogram matching algorithm](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.204.102&rep=rep1&type=pdf) to correct the scanner-dependent intensity variations
5. Normalization, we use [z-score algorithm](https://en.wikipedia.org/wiki/Standard_score) to do normalization sample by sample. Specifically, we calculate the mean value and std value from each sample data, and then every voxel value of this sample will subtract its mean value, divide its std value to obtain its normalized data.

<img src="https://user-images.githubusercontent.com/107039598/180916851-f35f07e0-551e-4f86-9613-72acb5a48738.png" width="60%" height="60%">



## How to use it: 
It depends on your task.
1. For ROI task, we recommend the process in roi_process.py, it contains 4 steps: Denoise, Bias field correction, Resampling and Normalization. All you need to do is to feed the MRI image (.nii) path, its corresponding mask (.nrrd) path, saved image path and saved mask path into the process function, then the program will produce the output image(.nii) and mask(.nrrd) as you desire.

2. For Whole-slide task, we recommend the process in whole-slide.

## Notice:
1. The mask you feed must be the binary mask, it means that there are only two kinds of value (0. and 1.) are acceptable, otherwise it will cause some problem in the N4 algorithm stage.
2. In resampling stage, the shape of the image and mask will both be changed, so don't use the original mask on the preprocessed imgae, they are not matched.
3. There might be some intermediate files due to the switching between different libraries.
4. It might take 3 to 5 minutes to process one sample, in which denoise stage and bias field correction take most of time.

## Prerequisites:
Need to install:
Dipy, SimpleITK, numpy, nibabel, nilearn.

That's all, feel free to use it!
If there is anything wrong with it, please let me know.
Thank you.
