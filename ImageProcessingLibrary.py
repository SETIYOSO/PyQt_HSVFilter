# import the necessary packages
import numpy as np
import cv2
import time

class HSVColorFilter(object):
	isImageIsValid = False
	isNotProcessing = True
	filteredImageData = 0

	def loadImage(self, filePath):
		self.imagePath = filePath
		#print self.imagePath
		self.originalImageData = cv2.imread(self.imagePath)
		if (self.originalImageData is not None):
			# Convert to HSV
			self.hsvImageData = cv2.cvtColor(self.originalImageData, cv2.COLOR_BGR2HSV)
			self.isImageIsValid = True
		else:
			self.isImageIsValid = False

		return self.isImageIsValid

	def filterImage(self, lower_threshold, upper_threshold):
		if self.isNotProcessing and self.isImageIsValid:
			self.isNotProcessing = False
			# print "lower threshold = " + str(lower_threshold)
			# print "upper threshold = " + str(upper_threshold)
			# time.sleep(4)
			lower = np.array(lower_threshold, dtype="uint8")
			upper = np.array(upper_threshold, dtype="uint8")

			mask = cv2.inRange(self.hsvImageData, lower, upper)
			self.filteredImageData = cv2.bitwise_and(self.hsvImageData, self.hsvImageData, mask = mask)
			# self.filteredImageData = self.originalImageData

			self.isNotProcessing = True
			return True
		else:
			return False

	def getFilteredImage(self):
		if self.filterImage is None:
			return 0
		else:
			return self.filteredImageData

	def getOriginalImage(self):
		return self.hsvImageData