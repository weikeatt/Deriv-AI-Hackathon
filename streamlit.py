import streamlit as st
import datetime
import pandas as pd
import os
import time
from PIL import Image
from io import BytesIO

# Import backend files
from DocumentAuthenticityAnalysis import highlight_pdf_annotations
from BankLogoValidity import main
from QRValidation import check_qr_code_for_bank
from OCRBalanceCheck import process_bank_statement
from HandwritingTensorflow import unseendata_test

st.set_page_config(layout="wide")
st.markdown(""" 
    <style>
        /* Target the p tag within the .st-emotion-cache-1puwf6r class */
        .st-emotion-cache-1puwf6r p {
            font-size: 20px;  /* Set font size to 20px */
            font-weight: bold;  /* Make the text bold */
        }

        .st-emotion-cache-1jicfl2 {
            padding-top: 15px;
            padding-bottom: 0px;
            margin-bottom: 0px !important;
        }
        . stVideo {
            width: 500px !important;
            height: 450px !important;
        }
    </style>
""", unsafe_allow_html=True)
st.title("֎ AI Solutions for User Authentication")
st.markdown("<div style='margin-bottom: 0px;'></div>", unsafe_allow_html=True)

# Set default values in session state if not already set
if "applicant_ID" not in st.session_state:
    st.session_state["applicant_ID"] = "A001"

if "full_name" not in st.session_state:
    st.session_state["full_name"] = "John Smith"

if "dob" not in st.session_state:
    st.session_state["dob"] = datetime.date(2000, 8, 18)

if "address" not in st.session_state:
    st.session_state["address"] = "No 1, Jalan 1, Taman Satu, 12345, Kedah"

if "employment_status" not in st.session_state:
    st.session_state["employment_status"] = "Employed"

# Create two columns for layout
col1, col2 = st.columns([1, 3])

# Left column: User details
with col1:
    st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    # User Profile Picture
    st.image("default_profile_picture.jpg", width=200)

    # Titles for Applicant ID, Full Name, and Date of Birth (display as normal text)
    st.markdown(f"**Applicant ID:** {st.session_state['applicant_ID']}")
    st.markdown(f"**Full Name:** {st.session_state['full_name']}")
    st.markdown(f"**Date of Birth:** {st.session_state['dob']}")

    # Address (display as normal text)
    st.markdown(f"**Address:** {st.session_state['address']}")

    # Employment Status (display as normal text)
    st.markdown(f"**Employment Status:** {st.session_state['employment_status']}")

# Right column: Tabs and content
with col2:
    tab1, tab2, tab3, tab4 = st.tabs(["Document Authenticity Analysis", "Profile Verification & Risk Assessment", "Text Recognition Model", "Adaptive Liveness Detection"])

    # Tab 1: Document Authenticity Analysis
    with tab1:
        st.header("Document Authenticity Analysis")

        # Load the PNG file in binary mode
        with open("FakeBankStatementScanned.png", "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="Download PNG",
                data=pdf_bytes,
                file_name="FakeBankStatementScanned.png",
                mime="application/png"
            )

        # Image and validation checks
        image_path = "FakeBankStatementScanned.png"
        emojis = ["📄", "✅", "✅", "✅", "✅", "✅", "✅"]  # List of emojis representing a true sign
        texts = [
            "Document Type: Bank Statement",
            "Text Alignment and Spacing Consistency",
            "Uniform Font Style and Overall Layout",
            "Valid Bank Logo",
            "QR Code is Scannable and Links to Official Bank Site",
            "Transaction Balance is Accurate and Tallies",
            "Name and Address Match User Input"
        ]

        # Highlight annotations and get the counts of shapes and text boxes
        annotations_count = highlight_pdf_annotations("FakeBankStatement.pdf", "FakeBankStatementScanned.pdf")
        shapes_count = annotations_count.get('shapes', 0)
        text_boxes_count = annotations_count.get('text_boxes', 0)

        # Change emoji based on the count of annotations
        if shapes_count > 0:
            emojis[1] = "❌"  # Change to red X if shapes are found
        if text_boxes_count > 0:
            emojis[2] = "❌"  # Change to red X if text boxes are found

        # Logo validation
        logo_valid = main("FakeBankStatement.pdf", "Official Logo/maybank.png", "Extracted Images", similarity_threshold=90)
        if not logo_valid:
            emojis[3] = "❌"  # Red X if logo is not valid

        # QR Code validation
        qr_valid = check_qr_code_for_bank("BankStatementQR.pdf", page_number=0)
        if not qr_valid:
            emojis[4] = "❌"  # Red X if QR code is invalid

        # OCR-based balance check
        balance_check_result = process_bank_statement("bankstatement.pdf", name="John Smith", address="No 1, Jalan 1, Taman Satu, 12345, Kedah")
        if not balance_check_result["balance_tallies"]:
            emojis[5] = "❌"  # Red X if balance check fails

        if not balance_check_result["name_present"] or not balance_check_result["address_present"]:
            emojis[6] = "❌"  # Red X if name or address is not found

        # Create two columns for image and emojis with text
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(image_path, width=300)

        with col2:
            for emoji, text in zip(emojis, texts):
                st.markdown(f"""
                    <div style='font-size: 1.2em; line-height: 1.2; padding: 8px 0;'>
                        {emoji} {text}
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    # Tab 2: Profile Verification & Risk Assessment
    with tab2:
        st.header("Profile Verification & Risk Assessment")

        # Check if the 'search_results.txt' file exists and has content
        file_path = 'search_results.txt'
        file_has_content = False
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read().strip()
                if content:
                    file_has_content = True

        # Define the emoji and message based on whether the file has content
        if file_has_content:
            emoji = "❌"
            message = "Public Data Profiling contains issues"
        else:
            emoji = "✅"
            message = "Public Data Profiling is Clean and Crime Free"

        # Display the status message with emoji and text
        col1, col2 = st.columns([1, 8])
        with col1:
            st.markdown(f"<div style='text-align: center; font-size: 2em;'>{emoji}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='padding: 10px 0; font-size: 1.2em;'>{message}</div>", unsafe_allow_html=True)

        st.header("Results:")
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Initialize an empty list to hold the titles and URLs
        links_data = []
        for i in range(0, len(lines), 3):
            title_line = lines[i].strip()
            url_line = lines[i + 1].strip()
            title = title_line.replace("Title: ", "").strip()
            url = url_line.replace("URL: ", "").strip()
            links_data.append({"Title": title, "Link": url})

        for index, item in enumerate(links_data, start=1):
            st.markdown(f'<p style="font-size: 20px;">{index}. <a href="{item["Link"]}" style="font-size: 20px; color: blue;">{item["Title"]}</a></p>', unsafe_allow_html=True)


        st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

    # Tab 3: Placeholder for any additional content
    # Tab 3: Placeholder for any additional content
    with tab3:
        # Display the header and instructions for Tab 3
        st.header("Text Recognition Model") 
        
        # File uploader for the user to upload an image
        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            # Try to open the image and handle errors
            try:
                # Read the uploaded file into a BytesIO object
                image = Image.open(BytesIO(uploaded_file.read()))
                
                # Display the uploaded image
                st.image(image, caption="Uploaded Image", use_container_width=True)  # Changed here
                
                # Save the uploaded file temporarily for processing
                image_path = "temp_image.jpg"
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Display a message while the model is loading/recognizing the text
                with st.spinner("Recognizing text, please wait..."):
                    # Simulate some delay (remove this in real use, it's for simulation)
                    time.sleep(2)  # This simulates loading time for your model
                    
                    # Call the unseendata_test method with the uploaded image
                    detected_alphabets = unseendata_test(image_path)

                # After model processing, display the results
                if detected_alphabets:
                    # Generate styled text with bold for detected alphabets and larger size for other characters
                    styled_text = "**Alphabets Detected:** "
                    for char in detected_alphabets:
                        # Make detected alphabets bold
                        if char.isalpha():  # Check if it's an alphabet
                            styled_text += f"**{char}** "  # Bold style
                        else:
                            # Make other characters larger
                            styled_text += f"<span style='font-size:30px'>{char}</span> "  # Larger size

                    # Display the styled result
                    st.markdown(styled_text, unsafe_allow_html=True)
                else:
                    st.write("No alphabets detected, please try again with a clearer image.")
            
            except Exception as e:
                # Handle the case when the file can't be opened as an image
                st.error(f"Error opening image: {e}")
    with tab4:
        video_file = open("demo.mp4", "rb")
        video_bytes = video_file.read()

        st.video(video_bytes)