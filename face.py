import cv2

import config


haar_faces = cv2.CascadeClassifier(config.HAAR_FACES)


def detect_single(image):
	"""Return bounds (x, y, width, height) of detected face in grayscale image.
	   If no face or more than one face are detected, None is returned.
	"""
	faces = haar_faces.detectMultiScale(image, 
				scaleFactor=config.HAAR_SCALE_FACTOR, 
				minNeighbors=config.HAAR_MIN_NEIGHBORS, 
				minSize=config.HAAR_MIN_SIZE, 
				flags=cv2.CASCADE_SCALE_IMAGE)
	if len(faces) != 1:
		return None
	return faces[0]
