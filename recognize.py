import keras
import cv2

img = cv2.imread('images/segmentdigit7.png')
h = keras.models.load_model('saved_model.h5')
y = h.predict(img.reshape(1, 28, 28, 1))