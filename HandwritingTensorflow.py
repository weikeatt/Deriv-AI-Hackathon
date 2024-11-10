import cv2
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt

# Load the model once when the script is executed
nn_model = load_model('handwritten_alphabet_model.h5')
alphabets = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def unseendata_test(filepath):
    """
    Function to process an input image, detect characters in it, and return the detected alphabets.
    
    Parameters:
    filepath (str): Path to the input image for alphabet detection.
    
    Returns:
    List: A list of detected alphabets.
    """
    
    # Read the input image
    image = cv2.imread(filepath)
    
    # Check if image is loaded successfully
    if image is None:
        print(f"Error: The image at '{filepath}' could not be loaded. Please check the file path.")
        return None
    
    # Convert the image to grayscale (remove the blur step)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding to make characters stand out (tune the threshold value as needed)
    _, thresh = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store preprocessed digits (characters)
    preprocessed_digits = []

    # Get bounding boxes of contours (characters)
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda b: b[1][0], reverse=False))

    # Process each contour (character)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        digit = thresh[y:y + h, x:x + w]
        
        # Resize and pad each detected digit (character)
        resized_digit = cv2.resize(digit, (18, 18))
        padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)
        
        preprocessed_digits.append(padded_digit)
    
    # Convert list of preprocessed digits to numpy array
    inp = np.array(preprocessed_digits)
    
    # List to store predicted alphabets
    alphabets_unseen = []

    # Prepare the plot for the detected characters
    figr = plt.figure(figsize=(len(inp), 4))
    
    # Loop through each preprocessed digit, predict and display the result
    for i, digit in enumerate(preprocessed_digits):
        [prediction] = nn_model.predict(digit.reshape(1, 28, 28, 1) / 255.)
        pred = alphabets[np.argmax(prediction)]
        alphabets_unseen.append(pred)
        
        figr.add_subplot(1, len(inp), i + 1)
        plt.xticks([]); plt.yticks([])  # Hide axis ticks
        plt.imshow(digit.reshape(28, 28), cmap="gray")
        plt.title(pred, color='green', fontsize=18, fontweight="bold")
    
    # Show the plot
    plt.show()
    
    # Return the list of detected alphabets
    return alphabets_unseen

# Example usage
# detected_alphabets = unseendata_test('Text Recognition Sample.jpg')
# if detected_alphabets:
#     print("Alphabets detected:", detected_alphabets)
