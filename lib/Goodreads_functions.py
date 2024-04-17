def get_title(soup):
    title = soup.find('h1',class_='Text Text__title1', attrs={'data-testid': 'bookTitle'}).get_text()
    return title

def get_ISBN(soup):
    try:
        isbn_element = soup.find('div', class_='BookPageMetadataSection__description').find('a')
        ISBN = isbn_element.text.strip().replace(" ", "").replace("ISBN","")
    except IndexError:
        ISBN = ""
    return ISBN

def get_author(soup):
    author = soup.find('span', class_="ContributorLink__name").get_text()
    return author

def get_genre(soup):
    genre_list = []
    try:
        genre_items = soup.find('ul', class_='CollapsableList').find_all('a')
        for genre_item in genre_items:
            genre_list.append(genre_item.text.strip())
        genres = ', '.join(genre_list)
    except TypeError:
        genres = ""
    return genres

def get_rating(soup):
    rating = soup.find('div', class_="RatingStatistics__rating").get_text()
    return rating

def get_rating_count(soup):
    rating_count=soup.find('span',attrs={'data-testid':'ratingsCount'}).get_text()
    rating_count=rating_count.split()[0]
    return

def get_reviews_count(soup):
    reviewer_count=soup.find('span',attrs={'data-testid':'reviewsCount'}).get_text()
    reviewer_count=reviewer_count.split()[0]
    return

def get_pages(soup):
    try:
        pagesFormat = soup.find('p', attrs={'data-testid': 'pagesFormat'}).get_text()
        pages = pagesFormat.split()[0]
    except AttributeError:
        pages = ""
    return pages

def get_format(soup):
    try: 
        pagesFormat = soup.find('p', attrs={'data-testid': 'pagesFormat'}).get_text()
        book_format = pagesFormat.split()[2]
    except AttributeError:
        book_format = ""
    return book_format

def get_published(soup):
    try:
        pass
    except IndexError:
        published = ""
    return published

def get_rewards(soup):
    return

def get_reviews(soup):
    pass
    return

def get_description(soup):
    pass
    return