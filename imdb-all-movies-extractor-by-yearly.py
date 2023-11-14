import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_imdb_movies(base_url):
    current_url = base_url

    # Create a session for making requests
    session = requests.Session()

    movie_info_list = []

    while current_url:
        # Use the session to reuse the underlying TCP connection
        response = session.get(current_url)

        # Use the 'lxml' parser for faster parsing
        soup = BeautifulSoup(response.content, "lxml")

        # Extract your desired information here
        # For example, you might want to extract movie titles, ratings, etc.
        # Update this part based on the structure of the IMDb page

        # For demonstration, let's extract movie titles
        movie_titles = soup.find_all("h3", {"class": "lister-item-header"})
        for title in movie_titles:
            movie_info_list.append(title.text.strip())

        # Find the "Next" link if it exists
        next_link = soup.find("a", {"class": "lister-page-next"})

        if next_link:
            next_url = urljoin(base_url, next_link["href"])
            current_url = next_url
        else:
            current_url = None

    return movie_info_list

# Streamlit app
st.title("IMDb Movie Scraper")

# Get base URL from user input
base_url = st.text_input("Enter IMDb base URL:", "https://www.imdb.com/search/title/?title_type=feature&year=2022-01-01,2022-12-31&start=1&ref_=adv_nxt")

# Button to trigger scraping
if st.button("Scrape IMDb"):
    st.text("Scraping... Please wait.")
    movie_list = scrape_imdb_movies(base_url)

    # Display the scraped movie titles
    if movie_list:
        st.text("Scraped Movie Titles:")
        for movie_title in movie_list:
            st.write(movie_title)
    else:
        st.text("No movies found.")

