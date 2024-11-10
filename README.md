# Deriv AI Hackathon

This project is an AI-driven solution for user authentication, developed using Python and the Streamlit framework. It offers real-time automation for document verification, profile authentication, risk assessment, and text recognition models.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Step 1: Run the Application' Data](#step-1-run-the-application)
- [File Structure](#file-structure)

## Installation📦

To install the required library (please install other libraries when module is not found), run:

```bash
pip install streamlit
```
## Usage📋
### Step 1: Run the Application

```bash
streamlit run streamlit.py
```

## File Structure📁

```
/Deriv
│
├── BankLogoValidity.py                   # Script to validate the bank logo in applicants' documents
├── DataExtractionFromFile.py             # Script to extract data from applicant's documents
├── DocumentAuthenticityAnalysis.py       # Script to verify the authenticity of submitted documents
├── HandwritingTensorflow.py              # Script for using pre-trained handwriting recognition model
├── MainOCR.py                            # Script for Optical Character Recognition (OCR) for text extraction
├── OCRBalanceCheck.py                    # Script to check the balance of bank statements via OCR
├── ProfileVerification.py                # Script to crawl Google using applicants' profiles with Selenium
├── QRValidation.py                       # Script for validating QR codes in submitted documents
├── Text Recognition AI Training.py       # Script for training AI model for text recognition (Download dataset from [Kaggle Handwritten Alphabets Dataset](https://www.kaggle.com/datasets/sachinpatel21/az-handwritten-alphabets-in-csv-format))
├── Text Recognition Sample.jpg           # Sample image for text recognition training
├── Utilities Statement.pdf               # Sample utility bill used for testing document analysis
├── default_profile_picture.jpg           # Default profile picture for applicants
├── handwritten_alphabet_model.h5         # Pre-trained model for handwriting recognition
├── search_results.txt                    # File to store search results
└── streamlit.py                          # Main entry point to run the web application using Streamlit
```
