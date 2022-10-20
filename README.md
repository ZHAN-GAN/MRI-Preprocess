# MRI-Preprocess

## Pipeline:
This is a MRI preprocessing pipeline for deep learning, which mainly took advices from [chapter 5](https://www.researchgate.net/publication/309640957_MRI_preprocessing) in Imaging Biomarkers.

It contains 5 steps:
1. Denoise, we use the [Non-Local Means algorithm](https://dipy.org/documentation/1.5.0/examples_built/denoise_nlmeans/#example-denoise-nlmeans) to remove the noise from images.
2. Bias field correction, we use [N4 algorithm](https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html) to correcting low frequency intensity non-uniformity present in MRI image data.
3. Resampling, we use the method described in this [blog](https://www.kaggle.com/code/mechaman/resizing-reshaping-and-resampling-nifti-files/notebook) to make voxel spcaing the same across samples, such that we could extract generalized features in the feature extraction stage.
4. Standardization, we use [nyul histogram matching algorithm](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.204.102&rep=rep1&type=pdf) to correct the scanner-dependent intensity variations, implementation of it refers to this [github](https://github.com/sergivalverde/MRI_intensity_normalization). 
5. Normalization, we use [z-score algorithm](https://en.wikipedia.org/wiki/Standard_score) to do normalization sample by sample. Specifically, we calculate the mean value and std value from each sample data, and then every voxel value of this sample will subtract its mean value, divide its std value to obtain its normalized data.

<img src="https://user-images.githubusercontent.com/107039598/180920498-d3f6760b-e77a-4e6a-aa89-795a12591d93.png" width="60%" height="60%">



## How to use it: 
It depends on your task.
1. For the Whole_slide task (it means you are not using part of the slice area), we recommend the process in whole_slide directory, it contains all the 5 steps above, but you have to be careful when you use it. Suppose you want to try the 5-fold cross validation, you have to prepare the training set and testing set of each fold in advance, cause the nyul algorithm have to train a histogram template based on the traning set. In detail, run the pre_nyul.py at first, then arrange the dataset in K-fold corss valiation way, after that, run the nyul_standardization.py to obtain the normalized MRI of K-fold.   

1. For the ROI task, we recommend you try both algorithms in whole_slide directory and roi directory, and use the better one. The process in roi_process.py performs better in my task, but I am not sure whether it will perform better on yours, it contains 4 steps: Denoise, Bias field correction, Resampling and Normalization (no Standardlization). All you need to do is to feed the MRI image (.nii) path, its corresponding mask (.nrrd) path, saved image path and saved mask path into the process function, then the program will produce the output image(.nii) and mask(.nrrd) as you desire.

## Notice:
1. The mask you feed must be the binary mask, it means that there are only two kinds of value (0. and 1.) are acceptable, otherwise it will cause some problem in the N4 algorithm stage.
2. In resampling stage, the shape of the image and mask will both be changed, so don't use the original mask on the preprocessed imgae, they are not matched.
3. There might be some intermediate files due to the switching between different libraries.
4. It might take 3 to 5 minutes to process one sample, in which denoise stage and bias field correction take most of time.

## Prerequisites:
Need to install:
Dipy, SimpleITK=2.0.2, numpy, nibabel, nilearn.

That's all, feel free to use it!
If there is anything wrong with it, please let me know.
Thank you.
