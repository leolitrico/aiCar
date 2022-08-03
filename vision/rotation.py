import numpy as np
import cv2

#rotate an image with the given rotationAngle
def rotate_image(image, rotationAngle):
  center = tuple(np.array(image.shape[1::-1]) / 2)
  rotationMatrix = cv2.getRotationMatrix2D(center, rotationAngle, 1.0)
  return cv2.warpAffine(image, rotationMatrix, image.shape[1::-1], flags=cv2.INTER_LINEAR)