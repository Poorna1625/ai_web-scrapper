import streamlit as st
from scrapy import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from reader import convert_html  # This function converts HTML to formatted output via ReaderLM-v2

def main():
    st.title("AI Web Scraper & Formatter")
    
    st.write("This app scrapes a website, cleans its content, and then uses AI (ReaderLM-v2) to convert the HTML into well-formatted markdown or JSON.")
    
    # Input URL from user.
    url = st.text_input("Enter Website URL", placeholder="https://example.com")
    
    # Button for starting the scraping process.
    if st.button("Scrape Website"):
        if not url:
            st.error("Please enter a valid URL.")
        else:
            try:
                st.info("Starting scraping process...")
                with st.spinner("Scraping the website..."):
                    raw_dom = scrape_website(url)

                with st.spinner("Extracting and cleaning body content..."):
                    body_html = extract_body_content(raw_dom)
                    cleaned_content = clean_body_content(body_html)
                
                # Store cleaned content in session state for later use.
                st.session_state["dom_content"] = cleaned_content

                st.success("Scraping successful!")
                with st.expander("View Cleaned Content"):
                    st.text_area("Scraped Content", cleaned_content, height=300)
            except Exception as e:
                st.error(f"An error occurred during scraping: {e}")
    
    # Once the DOM content is available, get the user's parsing instructions.
    if "dom_content" in st.session_state:
        st.subheader("Content Parsing Instructions")
        parse_instruction = st.text_area(
            "Describe what you want to extract (e.g., product prices, event details, Olympic medal counts, etc.):",
            placeholder="Enter your parsing instructions here..."
        )
        
        if st.button("Parse Content"):
            if not parse_instruction:
                st.error("Please provide parsing instructions.")
            else:
                try:
                    st.info("Starting parsing process...")
                    with st.spinner("Splitting content into manageable chunks..."):
                        # Split content in case it's lengthy.
                        dom_chunks = split_dom_content(st.session_state["dom_content"])
                    
                    with st.spinner("Converting HTML using AI (ReaderLM-v2)..."):
                        # Process each chunk and then aggregate results.
                        # Adjust your parse function if it can handle multiple chunks.
                        # For now, we'll simply process the first chunk.
                        # If needed, you can loop and combine outputs.
                        formatted_result = convert_html(dom_chunks[0])
                    
                    st.success("Parsing complete!")
                    st.subheader("AI Parsed Result")
                    st.text_area("Result", formatted_result, height=200)
                except Exception as e:
                    st.error(f"An error occurred during parsing: {e}")

if __name__ == "__main__":
    main()
