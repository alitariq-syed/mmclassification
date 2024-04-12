import numpy as np
import cv2

def rectilinear_projection(panorama, viewport_width, viewport_height, viewport_center_x, viewport_center_y, focal_length):
    # Calculate the half-width and half-height of the viewport
    half_width = viewport_width / 2
    half_height = viewport_height / 2

    # Calculate the pixel coordinates of the viewport corners
    top_left_x = int(viewport_center_x - half_width)
    top_left_y = int(viewport_center_y - half_height)
    bottom_right_x = int(viewport_center_x + half_width)
    bottom_right_y = int(viewport_center_y + half_height)

    # Create a blank image for the rectilinear projection
    projection_width = bottom_right_x - top_left_x
    projection_height = bottom_right_y - top_left_y
    projection = np.zeros((projection_height, projection_width, 3), dtype=np.uint8)

    # Perform rectilinear projection for each pixel in the viewport
    for y in range(top_left_y, bottom_right_y):
        for x in range(top_left_x, bottom_right_x):
            # Convert pixel coordinates to normalized coordinates in the range [-1, 1]
            u = (x - viewport_center_x) / half_width
            v = (y - viewport_center_y) / half_height

            # Calculate the polar coordinates
            theta = np.arctan2(u, focal_length)
            phi = np.arctan2(v, np.sqrt(u**2 + focal_length**2))

            # Convert polar coordinates to pixel coordinates in the panorama
            panorama_x = int((theta / (2 * np.pi) + 0.5) * panorama.shape[1])
            panorama_y = int((phi / np.pi + 0.5) * panorama.shape[0])

            # Copy the pixel from the panorama to the rectilinear projection
            if 0 <= panorama_y < panorama.shape[0] and 0 <= panorama_x < panorama.shape[1]:
                projection[y - top_left_y, x - top_left_x] = panorama[panorama_y, panorama_x]

    return projection


# Example usage
panorama = cv2.imread('panorama.png')
viewport_width = 640
viewport_height = 640
viewport_center_x = 320
viewport_center_y = 320
focal_length = 1000

projection = rectilinear_projection(panorama, viewport_width, viewport_height, viewport_center_x, viewport_center_y, focal_length)

import cv2
cv2.imwrite("projection.png",projection)

# cv2.imshow('Projection', projection)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
