import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image):
    """Blurs and then sharpens the image."""
    blurred = cv2.GaussianBlur(image, (51, 51), 0)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(blurred, -1, sharpen_kernel)
    return sharpened

def remove_unchanged(reference, current):
    """Removes unchanged parts of the current image by comparing with the reference image."""
    diff = cv2.absdiff(reference, current)  # Compute absolute difference
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)  # Threshold to get changes
    result = cv2.bitwise_and(current, current, mask=mask)  # Apply mask to current image
    return result, mask

def detect_large_color_regions(image, mask):
    """Detects large regions of red, yellow, and black in the given image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define color thresholds
    lower_red1, upper_red1 = np.array([0, 100, 100]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([160, 100, 100]), np.array([180, 255, 255])
    lower_yellow, upper_yellow = np.array([20, 100, 100]), np.array([30, 255, 255])
    lower_black, upper_black = np.array([0, 0, 0]), np.array([180, 255, 50])
    
    # Create masks for colors
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    
    # Combine color masks
    combined_mask = mask_red + mask_yellow + mask_black
    combined_mask = cv2.bitwise_and(combined_mask, mask)  # Apply change mask to remove small specks
    
    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw detected areas
    output = image.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    
    return output, combined_mask, contours

def display_results(reference, current, output, color_mask, original_reference, original_current):
    """Displays original images and detected changes."""
    plt.figure(figsize=(20, 5))
    
    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(original_reference, cv2.COLOR_BGR2RGB))
    plt.title("Reference Image")
    plt.axis("off")
    
    plt.subplot(1, 4, 2)
    plt.imshow(cv2.cvtColor(original_current, cv2.COLOR_BGR2RGB))
    plt.title("Current Image")
    plt.axis("off")
    
    plt.subplot(1, 4, 3)
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title("Subtracted Image")
    plt.axis("off")
    
    plt.subplot(1, 4, 4)
    plt.imshow(color_mask, cmap='gray')
    plt.title("Color Regions Mask")
    plt.axis("off")
    
    plt.show()

# Load images (Assume they exist in 'test_img/' folder)
reference_img = cv2.imread("test_img/TestImage1.jpg")
current_img = cv2.imread("test_img/TestImage2.jpg")

# Ensure images are loaded
if reference_img is None:
    print("Error: Could not load reference image.")
elif current_img is None:
    print("Error: Could not load current image.")
else:
    # Keep original images for display
    original_reference_img = reference_img.copy()
    original_current_img = current_img.copy()
    
    # Preprocess images
    reference_img = preprocess_image(reference_img)
    current_img = preprocess_image(current_img)
    
    result_img, change_mask = remove_unchanged(reference_img, current_img)
    output_img, color_mask, detected_contours = detect_large_color_regions(result_img, change_mask)
    display_results(original_reference_img, original_current_img, output_img, color_mask, original_reference_img, original_current_img)
