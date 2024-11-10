import cv2
import fitz  # PyMuPDF
import numpy as np
import re
from urllib.parse import urlparse

# List of official Malaysian bank domain names
malaysian_banks_domains = [
    "maybank2u.com.my",   # Maybank
    "cimb.com.my",        # CIMB
    "rhbgroup.com",       # RHB
    "publicbank.com.my",  # Public Bank
    "bankislam.com.my",   # Bank Islam
    "ambankgroup.com.my", # AmBank
    "hongleong.com.my",   # Hong Leong Bank
    "uob.com.my",         # UOB Malaysia
    "bsn.com.my",         # Bank Simpanan Nasional
    "bankrakyat.com.my",  # Bank Rakyat
    "bankmuhammadiah.com.my",  # Bank Muamalat Malaysia
    "kfh.com.my"          # Kuwait Finance House Malaysia
]

# Function to extract an image from a specific PDF page
def pdf_to_image(pdf_path, page_number=0, zoom_x=2.0, zoom_y=2.0):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)  # Load the specific page

    # Set zoom factor (for better quality)
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat)  # Extract image as Pixmap object

    # Convert Pixmap to NumPy array (OpenCV compatible format)
    img_data = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img_data.reshape(pix.height, pix.width, 3)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
    doc.close()

    return img

# Function to validate if the extracted value is a URL
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # match http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

# Function to extract the domain name from a URL
def get_domain_name(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc.lower()
    except Exception:
        return None

# Method to check if QR code contains a valid URL and if it's from an official Malaysian bank
def check_qr_code_for_bank(pdf_path, page_number=0):
    """
    Checks if the QR code extracted from a PDF contains a valid URL from an official Malaysian bank.

    Parameters:
        pdf_path (str): Path to the input PDF file.
        page_number (int): Page number to extract the QR code from (default is 0).

    Returns:
        bool: True if the QR code contains a valid URL from an official Malaysian bank, False otherwise.
    """
    try:
        # Load the PDF and convert the specified page to an image
        image = pdf_to_image(pdf_path, page_number)

        # Create a QRCodeDetector object
        detector = cv2.QRCodeDetector()

        # Detect and decode the QR code
        value, pts, qr_code = detector.detectAndDecode(image)

        # Check if QR code contains valid data and if the URL is valid
        if value and is_valid_url(value):
            domain = get_domain_name(value)
            if domain in malaysian_banks_domains:
                return True  # QR code contains a valid URL from an official Malaysian bank
        return False  # Either no QR code, invalid URL, or not a bank URL

    except Exception:
        return False  # In case of any error, return False

# Example usage:
# result = check_qr_code_for_bank("BankStatementQR.pdf", page_number=0)

# # Print the result
# print(result)
