import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import streamlit as st

# Function to scrape data from IMDb
def scrape_imdb(base_url):
    current_url = base_url

    # Create a session for making requests
    session = requests.Session()

    while current_url:
        # Use the session to reuse the underlying TCP connection
        response = session.get(current_url)

        # Use the 'lxml' parser for faster parsing
        soup = BeautifulSoup(response.content, "lxml")

        # Extract your desired information here
        # For example, you might want to extract movie titles, ratings, etc.
        # Modify this part based on your specific requirements

        # Find the "Next" link if it exists
        next_link = soup.find("a", {"class": "lister-page-next"})

        if next_link:
            next_url = urljoin(base_url, next_link["href"])
            current_url = next_url
            st.write(current_url)
        else:
            current_url = None

# Streamlit app
def main():
    st.title("IMDb Scraper")

    # Get base URL from user input
    base_url = st.text_input("Enter IMDb base URL:", "https://www.imdb.com/search/title/?title_type=feature&year=2022-01-01,2022-12-31&start=1&ref_=adv_nxt")

    # Button to start scraping
    if st.button("Scrape IMDb"):
        st.text("Scraping in progress...")
        scrape_imdb(base_url)
        st.text("Scraping completed!")

if __name__ == "__main__":
    main()
