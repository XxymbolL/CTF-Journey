import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image in grayscale
image = cv2.imread('Did You See It.png', cv2.IMREAD_GRAYSCALE)

# Function to extract and display bit planes
def show_bit_planes(image):
    bit_planes = []
    rows, cols = image.shape

    for i in range(8):
        # Extracting each bit plane by right-shifting the bits and masking the least significant bit
        bit_plane = (image >> i) & 1
        # Scale the bit plane to 0-255 for visibility (multiply by 255)
        bit_plane = np.uint8(bit_plane * 255)
        bit_planes.append(bit_plane)

        # Display each bit plane
        plt.subplot(2, 4, i+1)  # Create 2 rows and 4 columns for displaying 8 bit planes
        plt.imshow(bit_plane, cmap='gray')
        plt.title(f'Bit Plane {i}')
        plt.axis('off')

    plt.show()

# Call the function to display bit planes
show_bit_planes(image)

