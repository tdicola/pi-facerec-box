# Capture positive face recognition images
import glob
import os

import cv2

import picameracapture
import config
import face


DEBUG_IMAGE = 'capture.pgm'
POSITIVE_FILE_PREFIX = 'positive_'


# Find the largest ID of existing positive images.  Start new images
# after this ID value.
files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
count = 0
if len(files) > 0:
	count = int(files[-1][-7:-4])+1

cam = picameracapture.PiCameraCapture()

print 'Capturing positive training images.'
print 'Press button or type c (and press enter) to capture an image.'
print 'Press Ctrl-C to quit.'
while True:
	# Check if capture should be made.
	# TODO: Check if button is pressed.
	if raw_input() == 'c':
		image = cam.read()
		# Save image for debugging.
		cv2.imwrite(DEBUG_IMAGE, image)
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
		crop_height = int((config.FACE_HEIGHT / float(config.FACE_WIDTH)) * w)
		midy = y + h/2
		y1 = max(0, midy-crop_height/2)
		y2 = min(image.shape[0]-1, midy+crop_height/2)
		crop = image[y1:y2, x:x+w]
		# Save image to file.
		filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
		cv2.imwrite(filename, crop)
		print 'Wrote image', filename
		count += 1
