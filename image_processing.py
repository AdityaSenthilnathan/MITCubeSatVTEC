import cv2
import numpy as np
import matplotlib.pyplot as plt


def preprocess_image(image):
    blurred = cv2.GaussianBlur(image, (19, 19), 0)
    # Unsharp mask technique
    sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
    return blurred, sharpened


def remove_unchanged(reference, current):
    diff = cv2.absdiff(reference, current)  # Compute absolute difference
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)  # Threshold to get changes
    result = cv2.bitwise_and(current, current, mask=mask)  # Apply mask to current image
    return result, mask


def detect_large_color_regions(image, mask):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color thresholds with a wider range to capture varying fire and water colors
    lower_red1, upper_red1 = np.array([0, 50, 50]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([160, 50, 50]), np.array([180, 255, 255])
    lower_yellow, upper_yellow = np.array([15, 50, 50]), np.array([35, 255, 255])
    lower_blue, upper_blue = np.array([90, 50, 50]), np.array([130, 255, 255])
    lower_black, upper_black = np.array([0, 0, 0]), np.array([180, 255, 30])
    lower_grey, upper_grey = np.array([0, 0, 50]), np.array([180, 50, 200])  # Grey color range

    # Create masks for colors
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)

    # Combine color masks
    combined_mask = mask_red + mask_yellow + mask_black + mask_grey
    combined_mask = cv2.bitwise_and(combined_mask, mask)

    # Fill gaps in the mask and smooth edges
    kernel = np.ones((15, 15), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw detected areas
    output = image.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

    return output, combined_mask, contours


def display_results(reference, current, output, color_mask, original_reference, original_current, blurred_reference, blurred_current, sharpened_reference, sharpened_current, fire_status):
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
    white_pixels = np.sum(mask == 255)
    total_pixels = mask.size
    fire_percentage = (white_pixels / total_pixels) * 100
    if fire_percentage > 5:
        return f"fire detected: {fire_percentage:.2f}%"
    return f"no fire detected: {fire_percentage:.2f}%"


def possess_image(reference_img, current_img):
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
        output_img, color_mask, detected_contours = detect_large_color_regions(result_img, change_mask)

        # Check for fire detection
        fire_status = check_fire_detection(color_mask)

        display_results(original_reference_img, original_current_img, output_img, color_mask, original_reference_img, original_current_img, blurred_reference_img, blurred_current_img, sharpened_reference_img, sharpened_current_img, fire_status)