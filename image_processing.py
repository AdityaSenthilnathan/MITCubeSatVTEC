import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image):
    """Blurs and then sharpens the image using unsharp mask."""
    blurred = cv2.GaussianBlur(image, (71, 71), 0)
    # Unsharp mask technique
    sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
    return blurred, sharpened

def remove_unchanged(reference, current):
    """Removes unchanged parts of the current image by comparing with the reference image."""
    diff = cv2.absdiff(reference, current)  # Compute absolute difference
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)  # Threshold to get changes
    result = cv2.bitwise_and(current, current, mask=mask)  # Apply mask to current image
    return result, mask

def detect_large_color_regions(image, mask):
    """Detects large regions of red, yellow, blue, and brown in the given image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define color thresholds with a wider range to capture varying fire and water colors
    lower_red1, upper_red1 = np.array([0, 50, 50]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([160, 50, 50]), np.array([180, 255, 255])
    lower_yellow, upper_yellow = np.array([15, 50, 50]), np.array([35, 255, 255])
    lower_blue, upper_blue = np.array([90, 50, 50]), np.array([130, 255, 255])
    lower_brown, upper_brown = np.array([10, 100, 20]), np.array([20, 255, 200])
    
    # Create masks for colors
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    
    # Combine color masks
    combined_mask = mask_red + mask_yellow
    combined_mask = cv2.bitwise_and(combined_mask, mask)  # Apply change mask to remove small specks
    
    # Fill gaps in the mask and smooth edges
    kernel = np.ones((15, 15), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw detected areas
    output = image.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    
    return output, combined_mask, contours, mask_blue, mask_brown

def display_results(reference, current, output, color_mask, original_reference, original_current, blurred_reference, blurred_current, sharpened_reference, sharpened_current, fire_status):
    """Displays original images and detected changes."""
    plt.figure(figsize=(20, 10))
    
    plt.subplot(2, 4, 1)
    plt.imshow(cv2.cvtColor(original_reference, cv2.COLOR_BGR2RGB))
    plt.title("Reference Image")
    plt.axis("off")
    
    plt.subplot(2, 4, 2)
    plt.imshow(cv2.cvtColor(original_current, cv2.COLOR_BGR2RGB))
    plt.title("Current Image")
    plt.axis("off")
    
    plt.subplot(2, 4, 3)
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title("Subtracted Image")
    plt.axis("off")
    
    plt.subplot(2, 4, 4)
    plt.imshow(color_mask, cmap='gray')
    plt.title("Color Regions Mask")
    plt.axis("off")
    
    plt.subplot(2, 4, 5)
    plt.imshow(cv2.cvtColor(blurred_reference, cv2.COLOR_BGR2RGB))
    plt.title("Blurred Reference Image")
    plt.axis("off")
    
    plt.subplot(2, 4, 6)
    plt.imshow(cv2.cvtColor(blurred_current, cv2.COLOR_BGR2RGB))
    plt.title("Blurred Current Image")
    plt.axis("off")
    
    plt.subplot(2, 4, 7)
    plt.imshow(cv2.cvtColor(sharpened_reference, cv2.COLOR_BGR2RGB))
    plt.title("Sharpened Reference Image")
    plt.axis("off")
    
    plt.subplot(2, 4, 8)
    plt.imshow(cv2.cvtColor(sharpened_current, cv2.COLOR_BGR2RGB))
    plt.title("Sharpened Current Image")
    plt.axis("off")
    
    plt.suptitle(fire_status, fontsize=16, color='red')
    plt.text(0.5, 0.5, fire_status, fontsize=20, color='red', ha='center', va='center', transform=plt.gcf().transFigure)
    plt.show()

def check_fire_detection(mask):
    """Check if more than 5% of the image is white."""
    white_pixels = np.sum(mask == 255)
    total_pixels = mask.size
    fire_percentage = (white_pixels / total_pixels) * 100
    if fire_percentage > 5:
        return f"fire detected: {fire_percentage:.2f}%"
    return  f"no fire detected: {fire_percentage:.2f}%"

def check_water_detection(mask_blue, mask_brown):
    """Check if more than 50% of the image is blue or brown."""
    blue_pixels = np.sum(mask_blue == 255)
    brown_pixels = np.sum(mask_brown == 255)
    total_pixels = mask_blue.size
    water_percentage = ((blue_pixels + brown_pixels) / total_pixels) * 100
    if water_percentage > 50:
        return f"water detected: {water_percentage:.2f}%"
    return  f"no water detected: {water_percentage:.2f}%"

# Load images (Assume they exist in 'test_img/' folder)
reference_img = cv2.imread("test_img/HardTest2.jpg")
current_img = cv2.imread("test_img/HardTest6.jpg")

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
    blurred_reference_img, sharpened_reference_img = preprocess_image(reference_img)
    blurred_current_img, sharpened_current_img = preprocess_image(current_img)
    
    # Check differences on sharpened images
    result_img, change_mask = remove_unchanged(sharpened_reference_img, sharpened_current_img)
    output_img, color_mask, detected_contours, water_mask_blue, water_mask_brown = detect_large_color_regions(result_img, change_mask)
    
    # Check for fire and water detection
    fire_status = check_fire_detection(color_mask)
    water_status = check_water_detection(water_mask_blue, water_mask_brown)
    
    display_results(original_reference_img, original_current_img, output_img, color_mask, original_reference_img, original_current_img, blurred_reference_img, blurred_current_img, sharpened_reference_img, sharpened_current_img, fire_status + " | " + water_status)
