import cv2
import numpy as np

# Load image
img = cv2.imread('object.jpg')

# Pre-processing
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

# Object detection
cascade = cv2.CascadeClassifier('cascade.xml')
objects = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

# ROI selection
for (x,y,w,h) in objects:
    roi = edges[y:y+h, x:x+w]

# Line detection
lines = cv2.HoughLinesP(roi, rho=1, theta=np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)

# Check if slope is present
if lines is not None:
    print("Slope is present")
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)
        print("Slope: ", slope)
else:
    print("Slope is not present")
