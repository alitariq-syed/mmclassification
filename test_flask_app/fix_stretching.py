import cv2
import numpy as np

def fix_stretched_image(image):
    # Get the dimensions of the input image
    height, width = image.shape[:2]

    # Define the four corners of the distorted region
    distorted_corners = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Define the four corners of the desired rectangle
    target_corners = np.float32([[width * 0.2, height * 0.2],
                                 [width * 0.8, height * 0.2],
                                 [0, height],
                                 [width, height]])

    # Compute the perspective transformation matrix
    M = cv2.getPerspectiveTransform(distorted_corners, target_corners)

    # Apply the perspective transformation to the image
    fixed_image = cv2.warpPerspective(image, M, (width, height))

    return fixed_image

# Example usage
image = cv2.imread('panorama.png')
image = cv2.resize(image,[640,640])

fixed_image = fix_stretched_image(image)

import cv2
cv2.imwrite("fixed_image.png",fixed_image)

# Display the original and fixed images
# cv2.imshow('Original Image', image)
# cv2.imshow('Fixed Image', fixed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
