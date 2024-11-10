import fitz  # PyMuPDF
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta  # To handle accurate date differences

# Function to extract text from the PDF
def extract_text(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Extract text from each page
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extract text from the page

    # Replace multiple spaces with a single space and ensure proper line breaks
    text = ' '.join(text.split())  # Replace all whitespace sequences with a single space
    return text

# Function to check if a specific name is in the text
def is_name_present(text, name):
    # Check if the name appears in the text (case insensitive)
    return re.search(re.escape(name), text, re.IGNORECASE) is not None

# Function to check if a specific address is in the text
def is_address_present(text, address):
    # Check if the address appears in the text (case insensitive)
    return re.search(re.escape(address), text, re.IGNORECASE) is not None

# Function to extract the statement date
def extract_statement_date(text):
    # Regex pattern to match a date (e.g., MM/DD/YYYY or DD/MM/YYYY)
    date_pattern = re.compile(r"STATEMENT DATE\s*[:\-\s]*([0-9]{2}/[0-9]{2}/[0-9]{2,4})")
    date_match = re.search(date_pattern, text)

    if date_match:
        return date_match.group(1)  # Return the matched date (e.g., "31/10/24")
    return None

# Function to check if the document is a bank statement based on keywords
def is_bank_statement(text):
    # Regex patterns to search for "STATEMENT BALANCE" and "SAVINGS ACCOUNT"
    balance_pattern = re.compile(r"STATEMENT BALANCE", re.IGNORECASE)
    account_pattern = re.compile(r"SAVINGS ACCOUNT", re.IGNORECASE)
    
    # Search for keywords in the text
    if balance_pattern.search(text) and account_pattern.search(text):
        return True
    return False

# Function to check if the date is within the last 6 months
def is_within_last_6_months(statement_date_str):
    # Parse the statement date (assuming the format is DD/MM/YY or DD/MM/YYYY)
    try:
        statement_date = datetime.strptime(statement_date_str, "%d/%m/%y")  # Handle short year format (YY)
    except ValueError:
        statement_date = datetime.strptime(statement_date_str, "%d/%m/%Y")  # Handle full year format (YYYY)

    current_date = datetime.now()

    # Calculate the date 6 months ago using relativedelta for accurate month subtraction
    six_months_ago = current_date - relativedelta(months=6)
    
    # Compare year, month, and day
    if (statement_date.year > six_months_ago.year) or \
       (statement_date.year == six_months_ago.year and statement_date.month > six_months_ago.month) or \
       (statement_date.year == six_months_ago.year and statement_date.month == six_months_ago.month and statement_date.day >= six_months_ago.day):
        return True
    return False

# Function to extract and calculate total debits and credits from the OCR text
def calculate_transactions(text):
    # Regex pattern to match the transaction amounts with - or + signs
    transaction_pattern = re.compile(r"(\d+\.\d+)([+-])")  # This will match amounts like 10.10- or 19.08+
    amounts = re.findall(transaction_pattern, text)
    
    total_debits = 0
    total_credits = 0

    # Iterate over all the matched amounts
    for amount, sign in amounts:
        amount_value = float(amount)  # Convert amount to float
        if sign == '-':  # Debit (money going out)
            total_debits += amount_value
        elif sign == '+':  # Credit (money coming in)
            total_credits += amount_value
    
    # Calculate the total balance from the given "Ending Balance"
    ending_balance_pattern = re.compile(r"ENDING BALANCE\s*[:\-\s]*([\d,]+\.\d{2})")
    ending_balance_match = re.search(ending_balance_pattern, text)
    
    if ending_balance_match:
        ending_balance = float(ending_balance_match.group(1).replace(",", ""))
    else:
        return None, None, None

    return total_debits, total_credits, ending_balance

# Function to extract the starting balance
def extract_starting_balance(text):
    # Regex pattern to extract the starting balance (usually appears in a date line, or the first balance)
    starting_balance_pattern = re.compile(r"(\d+\.\d+)\s+\d{2}/\d{2}/\d{2}")  # Look for the first balance after the date
    starting_balance_match = re.search(starting_balance_pattern, text)
    
    if starting_balance_match:
        return float(starting_balance_match.group(1))
    return None

# Function to check if balances tally
def check_balance_tallies(starting_balance, total_debits, total_credits, ending_balance):
    if starting_balance is not None and ending_balance is not None:
        calculated_balance = starting_balance + total_credits - total_debits  # Balance calculation
        return abs(calculated_balance - ending_balance) < 0.01  # Allowing a small floating-point tolerance
    return False

def extract_ending_balance(text):
    # Regex pattern to match the "ENDING BALANCE"
    ending_balance_pattern = re.compile(r"ENDING BALANCE\s*[:\-\s]*([\d,]+\.\d{2})")
    ending_balance_match = re.search(ending_balance_pattern, text)
    
    if ending_balance_match:
        return float(ending_balance_match.group(1).replace(",", ""))
    return None

# Main method to process the bank statement
def process_bank_statement(pdf_path, name, address):
    # Extract the OCR text from the bank statement (PDF or image)
    ocr_text = extract_text(pdf_path)
    
    result = {
        "is_bank_statement": False,
        "statement_date": None,
        "is_within_last_6_months": False,
        "balance_tallies": False,
        "name_present": False,
        "address_present": False
    }

    # Check if the document is a bank statement
    if is_bank_statement(ocr_text):
        result["is_bank_statement"] = True
        
        # Extract statement date
        statement_date = extract_statement_date(ocr_text)
        if statement_date:
            result["statement_date"] = statement_date
            
            # Check if the statement date is within the last 6 months
            result["is_within_last_6_months"] = is_within_last_6_months(statement_date)

        # Extract the ending balance
        ending_balance = extract_ending_balance(ocr_text)
        # result["ending_balance"] = ending_balance

        # Extract the starting balance
        starting_balance = extract_starting_balance(ocr_text)
        # result["starting_balance"] = starting_balance

        # Calculate the debits, credits, and ending balance
        total_debits, total_credits, ending_balance = calculate_transactions(ocr_text)

        # Check if the balance tallies
        result["balance_tallies"] = check_balance_tallies(starting_balance, total_debits, total_credits, ending_balance)

        # Check if the name and address are present in the document
        result["name_present"] = is_name_present(ocr_text, name)
        result["address_present"] = is_address_present(ocr_text, address)

    return result

# pdf_path = "bankstatement.pdf"  # Path to your bank statement PDF
# name = ""  # Name to search for
# address = " # Address to search for
# # Call the function to process the bank statement
# result = process_bank_statement(pdf_path, name, address)

# # Print the results
# print(result)
