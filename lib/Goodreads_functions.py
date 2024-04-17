
from bs4 import BeautifulSoup as bs
import requests
import urllib.request

def get_title(soup):
    try:
        # Attempt to find the title element
        title_element = soup.find('h1', class_='Text Text__title1', attrs={'data-testid': 'bookTitle'})
        
        # Check if the element was found before attempting to get text
        if title_element is not None:
            title = title_element.get_text()
        else:
            title = "Title not found"  # or you could return None or any default value
    except Exception as e:
        # Handling any other exceptions that might occur
        print(f"An error occurred: {e}")
        title = "Error retrieving title"
    return title


def get_ISBN(soup):
    try:
        # Attempt to find the ISBN element
        isbn_element = soup.find('div', class_='BookPageMetadataSection__description').find('a')
        
        # Check if the element was found before accessing .text
        if isbn_element is not None:
            ISBN = isbn_element.text.strip().replace(" ", "").replace("ISBN", "")
        else:
            ISBN = "ISBN not found"
    except Exception as e:
        # Print error message for debugging
        print(f"An error occurred: {e}")
        ISBN = ""
    return ISBN

def get_author(soup):
    # Attempt to find the author element
    author_element = soup.find('span', class_="ContributorLink__name")
    
    # Check if the element was found before attempting to get text
    if author_element:
        return author_element.get_text()
    else:
        # Return a default value or raise a more specific error
        return "Author not found"

def get_genre(soup):
    genre_list = []
    try:
        # First, find the container with the class 'CollapsableList'
        genre_container = soup.find('ul', class_='CollapsableList')
        
        # Check if the container was found before proceeding
        if genre_container:
            genre_items = genre_container.find_all('a')
            for genre_item in genre_items:
                genre_list.append(genre_item.text.strip())
        else:
            print("Genre container not found")  # Optional: Log if the container wasn't found
    except Exception as e:
        print(f"Error extracting genres: {e}")

    return genre_list

def get_rating(soup):
    try:
        # Attempt to find the rating element
        rating_element = soup.find('div', class_="RatingStatistics__rating")
        
        # Check if the element was found before attempting to get text
        if rating_element:
            return rating_element.get_text().strip()
        else:
            # Log or handle the absence of the rating element
            print("Rating element not found")
            return "Rating not available"
    except Exception as e:
        print(f"Error extracting rating: {e}")
        return "Error retrieving rating"

def get_rating_count(soup):
    try:
        rating_count_element = soup.find('span', attrs={'data-testid': 'ratingsCount'})
        if rating_count_element:
            rating_count = rating_count_element.get_text().split()[0]
            return rating_count.replace(',', '')  # Remove commas for clean number format
        else:
            return "0"  # Return '0' or some other indicator that no ratings were found
    except Exception as e:
        print(f"Error extracting rating count: {e}")
        return "Error"  # Error handling or logging the issue

def get_reviews_count(soup):
    try:
        reviewer_count_element = soup.find('span', attrs={'data-testid': 'reviewsCount'})
        if reviewer_count_element:
            reviewer_count = reviewer_count_element.get_text().split()[0]
            return reviewer_count.replace(',', '')  # Remove commas for clean number format
        else:
            return "0"  # Return '0' or some other indicator that no reviews were found
    except Exception as e:
        print(f"Error extracting reviews count: {e}")
        return "Error"  # Error handling or logging the issue

def get_pages(soup):
    try:
        pagesFormat = soup.find('p', attrs={'data-testid': 'pagesFormat'}).get_text()
        pages = pagesFormat.split()[0].replace(",", "").strip()  # Remove commas and extra spaces
        if pages.isdigit():
            return pages
        else:
            return "N/A"  # Return 'N/A' if the split result isn't a number
    except AttributeError:
        return "N/A"  # Return 'N/A' if element or text is not found

def get_format(soup):
    try:
        pagesFormat = soup.find('p', attrs={'data-testid': 'pagesFormat'}).get_text()
        format_parts = pagesFormat.split()
        if len(format_parts) >= 3:
            return format_parts[2]  # Typically the third element is the format
        return "Format not specified"
    except AttributeError:
        return "Format not specified"
    except IndexError:
        return "Format not specified"

def get_publish_info(soup):
    try: 
        pub_info = soup.find('p', attrs={'data-testid': 'publicationInfo'}).get_text()
        return pub_info.strip()  # Clean whitespace for consistency
    except AttributeError:
        return "Publication info not available"


def get_description(soup):
    try:
        description_element = soup.find('span', class_="Formatted")
        if description_element:
            return description_element.get_text().strip()  # Remove excess whitespace
        return "No description available"
    except AttributeError:
        return "No description available"


def get_reviews(soup):
    pass
    return

def get_award_urls(url):
    urls=[]
    try:
        open_url = urllib.request.urlopen(url)
        soup = bs(open_url, 'html.parser')
        award_elements = soup.find_all('div', class_='category clearFix')

        # Extract URLs from award elements
        for element in award_elements:
            link = element.find('a', href=True)
            if link:
                urls.append('https://goodreads.com' + link['href'])

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return urls

def get_book_urls(url):
    urls = []

    try:
        open_url = urllib.request.urlopen(url)
        soup = bs(open_url, 'html.parser')
        book_links = soup.find_all('a', class_='pollAnswer__bookLink')

        # Extract URLs from book links
        for link in book_links:
            urls.append('https://goodreads.com' + link['href'])

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return urls

def get_book_urls_for_list(list_of_urls):
    all_urls = []
    for url in list_of_urls:
        urls = get_book_urls(url)
        all_urls.extend(urls)
    return all_urls