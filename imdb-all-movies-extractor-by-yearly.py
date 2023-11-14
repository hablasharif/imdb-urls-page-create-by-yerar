import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from datetime import datetime

def scrape_imdb_movies(base_url):
    current_url = base_url
    session = requests.Session()

    movie_info_list = []

    while current_url:
        response = session.get(current_url)
        soup = BeautifulSoup(response.content, "lxml")

        # Extract movie titles and IMDb links
        movie_elements = soup.find_all("h3", {"class": "lister-item-header"})
        for movie_element in movie_elements:
            # Extract movie title
            title = movie_element.a.text.strip()

            # Extract IMDb link
            imdb_link = urljoin(base_url, movie_element.a["href"])

            # Append title and IMDb link to the list
            movie_info_list.append({"title": title, "imdb_link": imdb_link})

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

    # Display the scraped movie titles and IMDb links
    if movie_list:
        st.text("Scraped Movie Titles and IMDb Links:")
        for movie_info in movie_list:
            st.write(f"Title: {movie_info['title']}")
            st.write(f"IMDb Link: {movie_info['imdb_link']}")
            st.write("-" * 50)

        # Save to CSV and provide download link
        filename = f"imdb_movies_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'imdb_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for movie_info in movie_list:
                writer.writerow(movie_info)

        st.markdown(f"Download the scraped data as CSV: [**{filename}**](/{filename})")
    else:
        st.text("No movies found.")
