import fitz  # PyMuPDF
import os
import imagehash
from PIL import Image
import numpy as np
import shutil

# Function to extract images from the PDF
def extract_images(pdf_path, image_folder):
    doc = fitz.open(pdf_path)

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    image_count = 0
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]  # Image reference
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Save the image to the image folder
            image_filename = f"image{image_count + 1}.png"
            image_path = os.path.join(image_folder, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            image_count += 1

    doc.close()

# Function to compare images based on their hash values and return if similarity is above threshold
def compare_images(location, folder_path, similarity_threshold=90, hash_size=8):
    threshold = 1 - similarity_threshold / 100
    diff_limit = int(threshold * (hash_size ** 2))

    # Get the hash of the location image (official logo)
    with Image.open(location) as img:
        hash1 = imagehash.average_hash(img, hash_size).hash

    fnames = os.listdir(folder_path)

    for image in fnames:
        # Skip non-image files
        if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            continue

        image_path = os.path.join(folder_path, image)

        with Image.open(image_path) as img:
            hash2 = imagehash.average_hash(img, hash_size).hash

            # Compare hashes and check if similarity is above the threshold
            diff = np.count_nonzero(hash1 != hash2)
            similarity_score = 100 * (1 - diff / (hash_size ** 2))

            if similarity_score >= similarity_threshold:
                # If similarity is above threshold, return True
                # print(f"Similarity score: {similarity_score:.2f}% - Match found!")
                return True  # Found a match with similarity > 90%
    
    # If no match found, return False
    return False

# Main function to extract and compare images, returning True if a match > 90% is found
def main(pdf_path, logo_path, output_folder, similarity_threshold=90):
    # Step 1: Extract images from the PDF
    extract_images(pdf_path, output_folder)

    # Step 2: Compare the extracted images with the official logo and check for matches
    return compare_images(logo_path, output_folder, similarity_threshold)


# Run the main method to check for similarity
# result = main("FakeBankStatement.pdf", "Official Logo/maybank.png", "Extracted Images", similarity_threshold=90)

# print(result)