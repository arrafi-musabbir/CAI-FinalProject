# -*- coding: utf-8 -*-
"""
Arrafi
10th April, 2021
"""

# Import the libary
import os
import SimpleITK as sitk
import cv2
import glob

# define a class
class main:

	# defining constructor method
	def __init__(self):

		# fixed/reference image path
		self.fixed_image_path = os.path.join(os.getcwd(),"Abdominal_Data/Reference/refLung_001.dcm")
		self.segmentAllImages()
		self.generateVideo()


	def iterateMovingImages(self):

		# list for storing all moving image paths
		self.moving_images = list()
		# moving image folder path
		moving_image_folder = os.path.join(os.getcwd(),"Abdominal_Data\\Moving")
		# iterating through all moving image and collecting their path
		for i in range(1,201):
			self.moving_images.append(moving_image_folder+"\\Moving_"+f"{i:03}"+"\\Moving_"+f"{i:03}"+".dcm")
		# return a list containing all moving image path
		return self.moving_images

	# this method segment a single image
	def segmentImage(self, moving_image_path, fixed_image_path):

		# Import images to register, pixel type Float32
		fixed_image = sitk.ReadImage(fixed_image_path, sitk.sitkFloat32)
		fixed_image2d = sitk.Extract(fixed_image, (fixed_image.GetWidth(), fixed_image.GetHeight(), 0), (0, 0, 0))
		moving_image = sitk.ReadImage(moving_image_path, sitk.sitkFloat32)
		moving_image2d = sitk.Extract(moving_image, (moving_image.GetWidth(), moving_image.GetHeight(), 0), (0, 0, 0))

		# Set up the registration
		registration_method = sitk.ImageRegistrationMethod()

		# Use mutual information metric
		registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins = 50)

		# Set initial transform
		initial_transform = sitk.CenteredTransformInitializer(fixed_image2d, moving_image2d, sitk.Similarity2DTransform())
		registration_method.SetInitialTransform(initial_transform)

		# Set optimizer
		registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate = 2.0, minStep = 0.001, 
		                                                             numberOfIterations = 100,
		                                                             gradientMagnitudeTolerance = 1e-8)
		# Scale the step size differently
		registration_method.SetOptimizerScalesFromIndexShift()

		# Use a linear interpolator
		registration_method.SetInterpolator(sitk.sitkLinear)

		# Execute the registration
		final_transform = registration_method.Execute(fixed_image2d, moving_image2d)

		# Verify the transformation result by applying it to align our images
		resampler = sitk.ResampleImageFilter()
		resampler.SetReferenceImage(fixed_image2d)
		resampler.SetInterpolator(sitk.sitkLinear)
		resampler.SetDefaultPixelValue(moving_image2d.GetPixelID())
		resampler.SetTransform(final_transform)
		moving_resampled = resampler.Execute(moving_image2d)

		# return resampled image
		return moving_resampled

	# this method segment all moving images alltogether
	def segmentAllImages(self):

		# defining resampled image path
		resampled_image_path = os.path.join(os.getcwd(),"Resampled_images")
		try:
			os.mkdir(resampled_image_path)
			print("Resampled_images directory created")
		except FileExistsError:
			print("directory already exists")
		# segment and resampling all the images
		print("starting image segmentation")
		for i in self.iterateMovingImages():
			image_path = resampled_image_path+"\\resampled"+i[-7:-4]+".png"
			sitk.WriteImage(sitk.Cast(sitk.RescaleIntensity(self.segmentImage(i, self.fixed_image_path)), sitk.sitkUInt8), image_path)
		return None

	# generates video from a series of images (.png/.jpg/.jpeg)
	def generateVideo(self):
		print("generating video from resampled images")
		# for storing all the images
		img_array = list()
		# iterate through the images and store it to an array
		for filename in glob.glob(os.path.join(os.getcwd(),'Resampled_images\\*.png')):
		    img = cv2.imread(filename)
		    height, width, layers = img.shape
		    size = (width,height)
		    img_array.append(img)
		# stacking the images together and writing it as a video
		# here 8 is the fps--  you can change the fps as you like
		out = cv2.VideoWriter('final-project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 8, size)
		for i in range(len(img_array)):
		    out.write(img_array[i])
		out.release()
		return None


if __name__ == '__main__':
	a = main()
	# a = 'musabbir'
	# print(a[-5:-2])

