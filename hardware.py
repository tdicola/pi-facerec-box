"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Class
Copyright 2013 Tony DiCola 
"""
import time

import cv2
import RPIO
from RPIO import PWM

import picam
import config
import face


class Box(object):
	"""Class to represent the state and encapsulate access to the hardware of 
	the treasure box."""
	def __init__(self):
		# Initialize lock servo and button.
		self.servo = PWM.Servo()
		RPIO.setup(config.BUTTON_PIN, RPIO.IN)
		# Set initial box state.
		self.button_state = RPIO.input(config.BUTTON_PIN)
		self.is_locked = None

	def lock(self):
		"""Lock the box."""
		self.servo.set_servo(config.LOCK_SERVO_PIN, config.LOCK_SERVO_LOCKED)
		self.is_locked = True

	def unlock(self):
		"""Unlock the box."""
		self.servo.set_servo(config.LOCK_SERVO_PIN, config.LOCK_SERVO_UNLOCKED)
		self.is_locked = False

	def is_button_up(self):
		"""Return True when the box button has transitioned from down to up (i.e.
		the button was pressed)."""
		old_state = self.button_state
		self.button_state = RPIO.input(config.BUTTON_PIN)
		# Check if transition from down to up
		if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
			# Wait 20 milliseconds and measure again to debounce switch.
			time.sleep(20.0/1000.0)
			self.button_state = RPIO.input(config.BUTTON_PIN)
			if self.button_state == config.BUTTON_UP:
				return True
		return False


if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'

	# Setup camera
	cam = picam.OpenCVCapture()

	box = Box()
	# Move box to locked position
	box.lock()

	print 'Running box...'
	print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
	print 'Press Ctrl-C to quit.'
	while True:
		# Check if capture should be made.
		# TODO: Check if button is pressed.
		if box.is_button_up():
			if not box.is_locked:
				# Lock the box if it is unlocked
				box.lock()
			else:
				# Check for the positive face and unlock if found.
				image = cam.read()
				# Convert image to grayscale.
				image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
				# Get coordinates of single face in captured image.
				result = face.detect_single(image)
				if result is None:
					print 'Could not detect single face!'
					continue
				x, y, w, h = result
				# Crop image to face.
				crop = face.crop(image, x, y, w, h)
				# Resize face to desired size.
				crop = cv2.resize(crop, 
						(config.FACE_WIDTH, config.FACE_HEIGHT), 
						interpolation=cv2.INTER_LANCZOS4)
				# Test face against model.
				[p_label, p_confidence] = model.predict(crop)
				print "Predicted label = %d (confidence=%.10f)" % (p_label, p_confidence)
				if p_label == config.POSITIVE_LABEL and p_confidence < config.POSITIVE_THRESHOLD:
					print 'Matched!'
					box.unlock()
				else:
					print 'Did not match!'
