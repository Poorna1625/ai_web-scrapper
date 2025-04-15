from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_website(url):
    """
    Launches a local headless Chrome browser using Selenium to fetch the page source.

    :param url: The website URL to scrape.
    :return: The HTML content of the page.
    """
    print("Starting local Chrome WebDriver...")
    
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    # Set up the ChromeDriver service; ensure that chromedriver is located in your project directory or in your PATH.
    service = Service(executable_path="./chromedriver.exe")
    
    # Launch the driver using the service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print(f"Navigating to {url}...")
    driver.get(url)
    
    # Wait to allow the page to load completely
    time.sleep(5)  # Adjust wait time if needed
    
    html = driver.page_source
    print("Page source obtained. Quitting WebDriver...")
    driver.quit()
    
    return html

def extract_body_content(html_content):
    """
    Extracts the <body> tag content from HTML.

    :param html_content: Raw HTML string.
    :return: String representation of the <body> content, or empty string if not found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    if body:
        return str(body)
    return ""

def clean_body_content(body_content):
    """
    Cleans the HTML body content by removing script and style tags and normalizes the text.

    :param body_content: HTML content of the body (as a string).
    :return: Cleaned text content.
    """
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Remove unwanted elements
    for tag in soup(["script", "style"]):
        tag.decompose()
    
    # Get plain text, preserving line breaks
    cleaned_text = soup.get_text(separator="\n")
    # Remove extra spaces and blank lines
    cleaned_text = "\n".join(line.strip() for line in cleaned_text.splitlines() if line.strip())

    # Optionally, filter out lines containing specific unwanted words
    filtered_lines = [
        line for line in cleaned_text.splitlines()
        if not any(unwanted in line.lower() for unwanted in ["cookie", "privacy policy", "consent"])
    ]
    
    return cleaned_text

def split_dom_content(dom_content, max_length=6000):
    """
    Splits the provided content into chunks of a maximum specified length (default 6000 characters).

    :param dom_content: The text content to split.
    :param max_length: Maximum length of each chunk.
    :return: List of content chunks.
    """
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]
