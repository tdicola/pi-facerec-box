# Train an eigenface recognizer that recognizes a specific face from positive and
# negative face images.
import fnmatch
import os

import cv2
import numpy as np

import config
import face


MEAN_FILE = 'mean.png'
POSITIVE_EIGENFACE_FILE = 'positive_eigenface.png'
NEGATIVE_EIGENFACE_FILE = 'negative_eigenface.png'


def walk_files(directory, match='*'):
	for root, dirs, files in os.walk(directory):
		for filename in fnmatch.filter(files, match):
			yield os.path.join(root, filename)

def prepare_image(filename):
	image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	image = cv2.resize(image, 
		(config.FACE_HEIGHT, config.FACE_WIDTH), 
		interpolation=cv2.INTER_LANCZOS4)
	return image

def normalize(X, low, high, dtype=None):
	"""Normalizes a given array in X to a value between low and high."""
	X = np.asarray(X)
	minX, maxX = np.min(X), np.max(X)
	# normalize to [0...1].
	X = X - float(minX)
	X = X / float((maxX - minX))
	# scale to [low...high].
	X = X * (high-low)
	X = X + low
	if dtype is None:
		return np.asarray(X)
	return np.asarray(X, dtype=dtype)


print "Reading training images..."
faces = []
labels = []
pos_count = 0
neg_count = 0
# Read all positive images
for filename in walk_files(config.POSITIVE_DIR, '*.pgm'):
	faces.append(prepare_image(filename))
	labels.append(config.POSITIVE_LABEL)
	pos_count += 1
# Read all negative images
for filename in walk_files(config.NEGATIVE_DIR, '*.pgm'):
	faces.append(prepare_image(filename))
	labels.append(config.NEGATIVE_LABEL)
	neg_count += 1
print 'Read', pos_count, 'positive images and', neg_count, 'negative images.'

# Train model
print 'Training model...'
model = cv2.createEigenFaceRecognizer()
model.train(np.asarray(faces), np.asarray(labels))

# Save model results
model.save(config.TRAINING_FILE)

print 'Training data saved to', config.TRAINING_FILE

# Save eignfaces and such
mean = model.getMat("mean")
eigenvectors = model.getMat("eigenvectors")

mean_norm = normalize(mean, 0, 255, dtype=np.uint8)
print 'Size', mean_norm.size, 'shape', mean_norm.shape
mean_resized = mean_norm.reshape(faces[0].shape)
print 'Size', mean_resized.size, 'shape', mean_resized.shape
cv2.imwrite(MEAN_FILE, mean_resized)

eigenvector_i = eigenvectors[:,0].reshape(faces[0].shape)
eigenvector_i_norm = normalize(eigenvector_i, 0, 255, dtype=np.uint8)
cv2.imwrite(POSITIVE_EIGENFACE_FILE, eigenvector_i_norm)

eigenvector_i = eigenvectors[:,1].reshape(faces[0].shape)
eigenvector_i_norm = normalize(eigenvector_i, 0, 255, dtype=np.uint8)
cv2.imwrite(NEGATIVE_EIGENFACE_FILE, eigenvector_i_norm)
