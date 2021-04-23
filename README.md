# CAI-FinalProject

The project consists in tracking the displacement of a region of interest on 2D ‘cine’ MR images. The displacement will be expressed relative to a ‘reference’ position defined on the 2D reference image.

You are provided:
- The ‘cine’ images
- The reference image
- The mask of the region of interest. The segmentation was performed on the reference image

You are expected to:
- (70 points) Write a python script such that when the script is run:
  o The region of interest is tracked on each ‘cine’ image
  o A video (.avi or .mp4) is generated. The video should display the segmentation of the region of interest on each cine image, as shown during Lecture 8
- (30 points) Write a 1 page paper (pdf file) with the following sections: introduction, methods, results, discussion

**Solution:**

Running Final-project.py script will segment and resample all the moving images and store them to a directory called Resampled_images. Then it will collect all the resamlped images and stack them together to form a .mp4 video file. 
