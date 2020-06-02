import cv2
import numpy

cam = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'SVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
while True:

    pass