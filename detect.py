# Import necessary libraries
import cv2
import numpy as np

# Load the image of the seed tray with plants
image = cv2.imread('plant2.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to create a binary image
_, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a mask for the holes
hole_mask = np.zeros_like(binary_image)

# Filter and draw only large enough contours (plants)
min_contour_area = 1000  # Adjust this threshold as needed
for contour in contours:
    if cv2.contourArea(contour) > min_contour_area:
            cv2.drawContours(hole_mask, [contour], -1, 255, thickness=cv2.FILLED)

            # Invert the mask to get the holes
            hole_mask = 255 - hole_mask

            # Now, you have a mask containing the holes in the seed tray
            # You can further process this mask for hole detection or use it as needed

            # Save or display the segmented image and the hole mask
            cv2.imwrite('segmented_plants.jpg', image)
            cv2.imwrite('hole_mask.jpg', hole_mask)