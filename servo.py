# Raspberry Pi Face Recognition Box Servo Calibration Sketch
# Copyright 2013 Tony DiCola

from RPIO import PWM

import config

servo = PWM.Servo()

print 'Servo Calibration'
print
print 'Use this tool to find the pulsewidth values which move the'
print 'lock latch to the locked and unlocked position. Update config.py'
print 'with the locked and unlocked servo pulsewidth values.'
print
print 'Values range from 1000 to 2000 (in microseconds), with 1500 being the center.'
print
print 'Press Ctrl-C to quit'
print 

while True:
	val = raw_input('Enter servo pulsewidth (1000 to 2000):')
	try:
		val = int(val)
	except ValueError:
		print 'Invalid value, must be between 1000 and 2000!'
		continue
	if val < 1000 or val > 2000:
		print 'Invalid value, must be between 1000 and 2000!'
		continue
	servo.set_servo(config.LOCK_SERVO_PIN, val)
