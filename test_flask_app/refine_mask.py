import cv2
import numpy as np

# Load the segmentation mask
mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)

# Apply morphological opening to remove small noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Apply morphological closing to fill small holes
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Apply contour detection to refine the mask
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if area < 1000: # adjust this value based on the size of the objects
        cv2.drawContours(mask, [contours[i]], 0, 0, -1)
		
		
		
################


import cv2
import numpy as np

# Load the segmentation mask
mask = cv2.imread('path/to/mask.png', cv2.IMREAD_GRAYSCALE)

# Define the kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Perform opening to remove small clusters
mask_opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Save the result
cv2.imwrite('path/to/mask_opened.png', mask_opened)