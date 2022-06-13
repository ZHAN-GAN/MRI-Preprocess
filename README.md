# MRI-Preprocess

## Pipeline:
This is a MRI preprocessing pipeline for deep learning, which mainly took advices from chapter [5](https://www.researchgate.net/publication/309640957_MRI_preprocessing) in Imaging Biomarkers.

It contains 4 steps:
1. Denoise, we use the [Non-Local Means algorithm](https://dipy.org/documentation/1.5.0/examples_built/denoise_nlmeans/#example-denoise-nlmeans) to remove the noise from images.
2. Bias field correction, we use [N4 algorithm](https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html) to correcting low frequency intensity non-uniformity present in MRI image data.
3. Resampling, we use the method described in this [blog](https://www.kaggle.com/code/mechaman/resizing-reshaping-and-resampling-nifti-files/notebook) to make voxel spcaing the same across samples, such that we could extract generalized features in the feature extraction stage.
4. Normalization, we use [z-score algorithm](https://en.wikipedia.org/wiki/Standard_score) to do normalization sample by sample. Specifically, we calculate the mean value and std value from each sample data, and then every voxel value of this sample will subtract its mean value, divide its std value to obtain its normalized data.

<img src="https://user-images.githubusercontent.com/107039598/173266497-64f18cf1-bf8d-4e23-8f4d-56bd86b7b35b.png" width="60%" height="60%">


## How to use it:
All you need to do is to feed the MRI image (.nii) path, its corresponding mask (.nrrd) path, saved image path and saved mask path into the process function, then the program will produce the output image(.nii) and mask(.nrrd) as you desire.

## Notice:
1. The mask you feed must be the binary mask, it means that there are only two kinds of value (0. and 1.) are acceptable, otherwise in the N4 algorithm stage, it will cause some problem.
2. In resampling stage, the shape of the image and mask will both be changed, so don't use the original mask on the preprocessed imgae, theny are not matched.
3. There might be some intermediate files due to the conversion between different libraries.
4. It might take 3 to 5 minutes to process one sample, in which denoise stage and bias field correction take most of time.

## Prerequisites
Need to install:
Dipy, SimpleITK, numpy, nibabel, nilearn.

That's all, feel free to use it!
If there is anything wrong with it, please let me know.
Thank you.
