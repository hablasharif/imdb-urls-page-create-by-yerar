import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_movie_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract your desired information here
    # For example, you might want to extract movie titles, ratings, etc.
    # Replace the following lines with your actual extraction logic
    movie_titles = [title.text for title in soup.find_all("h3", class_="lister-item-header")]

    return movie_titles

def main():
    st.title("IMDb Movie Scraper")

    # Input for base URL
    base_url = st.text_input("Enter IMDb Base URL:", "https://www.imdb.com/search/title/?title_type=feature&year=2022-01-01,2022-12-31")

    if st.button("Scrape Movies"):
        increment = 50  # Increment by 50 to get the desired page numbers
        results_per_page = 50  # Number of results per page
        total_results = 10000  # Total number of results
        num_links = total_results // results_per_page  # Calculate the number of links based on total results

        movie_data = []

        # Progress bar
        progress_bar = st.progress(0)

        for i in range(increment + 1, num_links * increment + 1, increment):
            url = f"{base_url}&start={i}&ref_=adv_nxt"
            movie_data.extend(get_movie_data(url))

            # Update progress bar
            progress_percentage = i / (num_links * increment) * 100
            progress_bar.progress(progress_percentage)

        st.write(f"Number of movies: {len(movie_data)}")

        # Display the extracted movie titles
        st.write("Movie Titles:")
        st.write(movie_data)

if __name__ == "__main__":
    main()
