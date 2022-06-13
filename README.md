# MRI-Preprocess
 
This is a MRI preprocessing pipeline for deep learning, which mainly took advices from chapter [5](https://www.researchgate.net/publication/309640957_MRI_preprocessing) in Imaging Biomarkers.

It contains 4 steps:
1. Denoise, we use the [Non-Local Means algorithm](https://dipy.org/documentation/1.5.0/examples_built/denoise_nlmeans/#example-denoise-nlmeans) to remove the noise from images.
2. Bias field correction, we use [N4 algorithm](https://simpleitk.readthedocs.io/en/master/link_N4BiasFieldCorrection_docs.html) to correcting low frequency intensity non-uniformity present in MRI image data.
3. Resampling, we use the method described in this [blog](https://www.kaggle.com/code/mechaman/resizing-reshaping-and-resampling-nifti-files/notebook) to make voxel spcaing the same across samples, such that we could extract generalized features in the feature extraction stage.
4. Normalization, we use [z-score algorithm](https://en.wikipedia.org/wiki/Standard_score) to do normalization sample by sample. Specifically, we calculate the mean value and std value from each sample data, and then every voxel value of this sample will subtract its mean value, divide its std value to obtain its normalized data.

<div style="width: 60%; height: 60%">
 ![image](https://user-images.githubusercontent.com/107039598/173265654-801bb92a-82e7-4517-bd9a-d43a6a440fc7.png)
</div>
