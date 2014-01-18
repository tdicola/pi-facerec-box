
# Size (in pixels) to resize images for training and prediction.
FACE_WIDTH = 92
FACE_HEIGHT = 112

# Location of positive and negative training images.
POSITIVE_DIR = './training/positive'
NEGATIVE_DIR = './training/negative'

# Value for positive and negative labels passed to face recognition model.
# Can be any integer values, but must be unique from each other.
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2

POSITIVE_THRESHOLD = 3000.0

# File to save and load face recognizer model.
TRAINING_FILE = 'training.xml'

# Face detection cascade classifier configuration.
HAAR_FACES = 'haarcascade_frontalface_alt.xml'
#HAAR_FACES = './haarcascades/haarcascade_frontalface_default.xml'
HAAR_SCALE_FACTOR = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE = (30, 30)

# Lock servo configuration.
LOCK_SERVO_PIN = 18
LOCK_SERVO_UNLOCKED = 2000
LOCK_SERVO_LOCKED = 1100

# Other hardware configuration.
BUTTON_PIN = 25
BUTTON_DOWN = False # Low signal
BUTTON_UP = True # High signal