import time

import cv2
import RPIO
from RPIO import PWM

import picameracapture
import config
import face


DEBUG_IMAGE = 'capture.pgm'


# Load training data into model
print 'Loading training data...'
model = cv2.createEigenFaceRecognizer()
model.load(config.TRAINING_FILE)
print 'Training data loaded!'

# Setup camera
cam = picameracapture.PiCameraCapture()

# Setup lock servo and button
servo = PWM.Servo()
RPIO.setup(config.BUTTON_PIN, RPIO.IN)

# Setup current state.
button_state = RPIO.input(config.BUTTON_PIN)
islocked = None

# TODO: Refactor this into a box class that handles moving the servo and reading the button.
def lock():
	global islocked
	# Move servo to lock position
	servo.set_servo(config.LOCK_SERVO_PIN, config.LOCK_SERVO_LOCKED)
	islocked = True

def unlock():
	global islocked
	# Move servo to lock position
	servo.set_servo(config.LOCK_SERVO_PIN, config.LOCK_SERVO_UNLOCKED)
	islocked = False

def button_up():
	global button_state
	old_state = button_state
	button_state = RPIO.input(config.BUTTON_PIN)
	# Check if transition from down to up
	if old_state == config.BUTTON_DOWN and button_state == config.BUTTON_UP:
		# Wait 20 milliseconds and measure again to debounce switch.
		time.sleep(20.0/1000.0)
		button_state = RPIO.input(config.BUTTON_PIN)
		if button_state == config.BUTTON_UP:
			print 'Button pressed!'
		return button_state == config.BUTTON_UP
	return False

# Move box to locked position
lock()

print 'Running box...'
print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
print 'Press Ctrl-C to quit.'
while True:
	# Check if capture should be made.
	# TODO: Check if button is pressed.
	if button_up():
		if not islocked:
			# Lock the box if it is unlocked
			lock()
		else:
			# Check for the positive face and unlock if found.
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
			# Resize face to desired size.
			crop = cv2.resize(crop, 
					(config.FACE_HEIGHT, config.FACE_WIDTH), 
					interpolation=cv2.INTER_LANCZOS4)
			# Test face against model.
			[p_label, p_confidence] = model.predict(crop)
			print "Predicted label = %d (confidence=%.10f)" % (p_label, p_confidence)
			if p_label == config.POSITIVE_LABEL and p_confidence < config.POSITIVE_THRESHOLD:
				print 'Matched!'
				unlock()
			else:
				print 'Did not match!'
