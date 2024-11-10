import cv2
import easyocr
import re

# Initialize EasyOCR reader (GPU-enabled if available)
reader = easyocr.Reader(['en'], gpu=True)
keywords = ["driving licence", "national identity", "national card", "kad pengenalan", "card"]

def extract_text_and_check_keywords(image_path, keywords):
    """
    Extracts text from an image using OCR and checks for specific keywords.
    
    Parameters:
        image_path (str): Path to the input image.
        keywords (list): List of keywords to search for in the extracted text.
    
    Returns:
        tuple: (bool, bool, list)
            - Boolean indicating if any of the keywords were found.
            - Boolean indicating if "national card" or related keywords were found.
            - List of detected text (without bounding boxes or confidence scores).
    """
    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoising and enhancing contrast for better OCR results
    gray = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

    # Thresholding to get a binary image (adaptive thresholding)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Use EasyOCR to detect text from the entire image
    result = reader.readtext(thresh, detail=0)  # Use detail=0 to return only the text

    # Function to check if any of the keywords are present in the extracted text
    def contains_keywords(text, keywords):
        """
        Check if any of the keywords are present in the extracted text.
        Returns True if any keyword is found, False otherwise.
        """
        for keyword in keywords:
            if re.search(keyword, text, re.IGNORECASE):
                return True
        return False

    # Initialize national card variable
    national_card = False
    found_keywords = False

    # Check for keywords in the detected text
    for text in result:
        if contains_keywords(text, keywords):
            found_keywords = True
            if contains_keywords(text, keywords):
                national_card = True
            break  # Stop after finding the first match

    # Return whether keywords were found, national_card status, and the list of detected text
    return found_keywords, national_card, result


# Call the function to extract text and check for keywords
# found_keywords, national_card, result = extract_text_and_check_keywords('NationalIC.png', keywords)

# # Print the results
# print(f"National card related keywords found: {national_card}")

# # Print the detected text (without bounding boxes or confidence scores)
# for text in result:
#     print(f"Detected text: {text}")
