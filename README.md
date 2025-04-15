AI Web Scraper & Formatter


This repository contains an interactive, AI-powered web scraping and formatting tool. The tool uses Selenium and BeautifulSoup to scrape and clean website content, and it leverages ReaderLM‑v2 (a 1.5B parameter language model from Jina AI) to convert raw HTML into well-formatted Markdown (or JSON) output, as well as to generate concise summaries of the content. An interactive Streamlit interface ties everything together for easy usage.

Features
Web Scraping:
Uses Selenium to launch a headless Chrome browser to scrape website content. Functions in scrapy.py extract the HTML, isolate the <body> content, and perform cleaning (removing scripts, styles, comments, etc.).

Content Formatting:
The module in reader.py loads ReaderLM‑v2 to process cleaned HTML. It creates clear prompts (with markers like Output:) to instruct the model to output only formatted markdown or JSON.

Summarization:
A summarization function in reader.py further processes the formatted content to generate a concise summary.

Interactive UI:
The readerlm_app.py file integrates the web scraping and AI formatting pipeline into an interactive Streamlit application, allowing users to:

Input a website URL.

View the scraped and cleaned content.

Get a formatted output (Markdown/JSON).

Request a summary of the content.

Directory Structure
scrapy.py:
Contains functions to scrape a website using Selenium, extract the <body> content, clean the text using BeautifulSoup, and split the text into manageable chunks.

reader.py:
Loads the ReaderLM‑v2 model and tokenizer, defines functions to clean HTML, create prompts, convert HTML to formatted Markdown (or JSON), and summarize text.

readerlm_app.py:
A Streamlit application that brings together the scraping and formatting/summarization modules to provide an interactive interface.

requirements.txt:
Lists all the dependencies needed for the project.

Prerequisites
Python 3.8+

Chrome Browser and ChromeDriver:
Ensure that ChromeDriver is installed and available in your project directory or PATH. You can download ChromeDriver from here.

GPU (Optional):
While the model will work on CPU, it is recommended to use a GPU for faster generation.

Install the required dependencies:

bash
Copy
pip install -r requirements.txt
Running the Application
Test the Conversion/Summarization Module
To run a standalone test of the AI conversion and summarization functions, execute:

bash
Copy
python reader.py
This will process an example HTML snippet and print the formatted output and a summary in the terminal.

Launch the Interactive Streamlit App
To run the full interactive web interface, execute:

bash
Copy
streamlit run readerlm_app.py
Scrape Website:
Enter a valid URL and click "Scrape Website" to fetch and clean the website's HTML content.

Parse Content:
Once the content is scraped, provide parsing instructions (e.g., “extract headlines” or “get product prices”) and click "Parse Content" to have the AI model convert the HTML into formatted output.

View Result:
The formatted output (and summary if implemented) will be displayed in the app interface.

Example Websites for Testing
You can use the following websites to practice scraping:

quotes.toscrape.com – A site designed for scraping practice.

books.toscrape.com – Another site designed for learning web scraping.

news.ycombinator.com – For practicing with news headlines.

Note: Always check the website’s robots.txt and terms of service before scraping.

Contributing
Contributions are welcome! Feel free to open issues or pull requests with improvements, bug fixes, or suggestions.

License
This project is released under the MIT License. See the LICENSE file for details.

Acknowledgments
ReaderLM‑v2: Thanks to Jina AI for developing this powerful language model.

Selenium & BeautifulSoup: For providing robust web scraping and HTML parsing capabilities.

Streamlit: For the interactive, easy-to-use UI framework.


