import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of crime-related keywords
crime_keywords = [
    "Murder", "Assault", "Theft", "Robbery", "Fraud", "Forgery", "Kidnapping",
    "Arson", "Smuggling", "Cybercrime", "Bribery", "Extortion", "Embezzlement",
    "Human Trafficking", "Drug Trafficking", "Vandalism", "Domestic Violence",
    "Money Laundering", "Homicide", "Burglary", "Blackmail", "Assassination",
    "Sexual Assault", "Shoplifting", "Identity Theft", "Impersonation", "Corruption",
    "Stalking", "Illegal Possession of Weapons", "Hit-and-Run", "Attempted Murder", 
    "Political Scandal", "Sexual Harassment", "Corporate Scandal", "Financial Scandal",
    "Fraudulent Claims", "False Accusations", "Abuse of Power", "Corruption"
]

# Set up Selenium WebDriver (using Chrome)
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode (without UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (optional)
    
    # Set up ChromeDriver using webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Function to search for crime-related keywords combined with a person's name and extract text from a specific class
def search_and_extract_text_for_person(name, max_results=10, file_name="search_results.txt"):
    driver = setup_driver()

    results_collected = 0  # To count how many results we've gathered

    try:
        # Open the file to write the results
        with open(file_name, 'a', encoding='utf-8') as file:
            for keyword in crime_keywords:
                if results_collected >= max_results:  # Stop if we have already collected the max number of results
                    break

                # Combine the person's name with the crime-related keyword
                search_query = f'"{name}" {keyword}'
                search_url = f"https://www.google.com/search?q={search_query}"
                driver.get(search_url)

                # Wait for the search results to load and find the titles
                WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tF2Cxc")))

                # Find elements with the class 'tF2Cxc' (updated Google class for search result items)
                search_results = driver.find_elements(By.CLASS_NAME, 'tF2Cxc')

                if search_results:  # Only process if titles are found
                    # Loop through the search results and check if any title contains a crime keyword
                    for result in search_results:
                        # Extract the title text
                        title = result.find_element(By.CLASS_NAME, 'LC20lb').text
                        # Extract the URL (from the <a> tag)
                        url = result.find_element(By.XPATH, ".//a").get_attribute("href")

                        # Log the title and URL for debugging
                        print(f"Title: {title}")
                        print(f"URL: {url}")

                        # Check if the title contains any crime-related keyword
                        match_found = any(crime.lower() in title.lower() for crime in crime_keywords)

                        # If a match is found, write it to the file
                        if match_found:
                            file.write(f"Title: {title}\n")
                            file.write(f"URL: {url}\n")
                            file.write("-" * 80 + "\n")  # Separator between results
                            results_collected += 1

                        # Stop collecting once we've reached the desired number of results
                        if results_collected >= max_results:
                            break

                time.sleep(2)  # Adding delay to avoid getting blocked

    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Close the driver
        driver.quit()

# Example function to call
def search_crime_news_for_person(name):
    # Write the results to a text file
    search_and_extract_text_for_person(name, max_results=10, file_name="search_results.txt")

    print(f"Results saved to 'search_results.txt'.")

# Example usage:
# search_crime_news_for_person("John Smith")
