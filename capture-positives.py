"""Raspberry Pi Face Recognition Treasure Box
Positive Image Capture Script
Copyright 2013 Tony DiCola 

Run this script to capture positive images for training the face recognizer.
"""
import glob
import os

import cv2

import config
import face


# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'


if __name__ == '__main__':
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, 
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	camera = config.CAMERA
	print 'Capturing positive training images.'
	print 'Press button or type c (and press enter) to capture an image.'
	print 'Press Ctrl-C to quit.'
	while True:
		# Check if capture should be made.
		# TODO: Check if button is pressed.
		if raw_input() == 'c':
			image = camera.read()
			# Convert image to grayscale.
			image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
			# Get coordinates of single face in captured image.
			result = face.detect_single(image)
			if result is None:
				print 'Could not detect single face!'
				continue
			x, y, w, h = result
			# Crop image as close as possible to desired face aspect ratio.
			# Might be smaller if face is near edge of image.
			crop = face.crop_face(image, x, y, w, h)
			# Save image to file.
			filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
			cv2.imwrite(filename, crop)
			print 'Wrote image', filename
			count += 1
