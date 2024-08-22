from bs4 import BeautifulSoup
import requests
import time
import random
from urllib.parse import urljoin
from datetime import datetime
from news.models import Article, Tag

import os


def get_month_number(month):
    """
       Convert Persian month names to their corresponding month numbers.

       Args:
           month (str): The Persian name of the month.

       Returns:
           int: The month number (1-12) or None if the month name isn't recognized.
       """
    month_mapping = {
        'فروردین': 1,
        'اردیبهشت': 2,
        'خرداد': 3,
        'تیر': 4,
        'مرداد': 5,
        'شهریور': 6,
        'مهر': 7,
        'آبان': 8,
        'آذر': 9,
        'دی': 10,
        'بهمن': 11,
        'اسفند': 12,
    }
    return month_mapping.get(month)


def extract_article_data(link):
    """
        Scrape article data from a given link. This gets the title, tags, author, content, and publication date.

        Args:
            link (str): The URL of the article to scrape.

        Returns:
            tuple: Contains title (str), tags (list), writer (str), content (list of paragraphs), and published_date (datetime).
        """
    try:
        page = BeautifulSoup(requests.get(link).content, "html.parser")
        title = page.find('article').find('h1').text
        tags = [tag.text for tag in
                page.findAll('span', class_="typography__StyledDynamicTypographyComponent-t787b7-0 cHbulB")]
        try:
            writer = page.find('span', class_="typography__StyledDynamicTypographyComponent-t787b7-0 kZjgvK").text
        except:
            writer = None

        try:
            published_date = page.find('span',
                                       class_="typography__StyledDynamicTypographyComponent-t787b7-0 fTxyQo fa").text
            date_parts = published_date.split(' ')
            day = int(date_parts[1])
            month = get_month_number(date_parts[2])
            year = int(date_parts[3])
            time_parts = date_parts[5].split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            published_date = datetime(year, month, day, hour, minute)


        except:
            published_date = None

        content = [p.text for p in page.find_all('p',
                                                 class_="typography__StyledDynamicTypographyComponent-t787b7-0 fZZfUi ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU")]

        return title, tags, writer, content, published_date
    except Exception as e:
        print(f"Error extracting data from {link}: {e}")
        return None, None, None, None, None


def scrape_zoomit(start_page=1, end_page=500):
    """
       Scrape multiple pages of articles from Zoomit and save them to the database.

       This function iterates over a range of pages, scrapes articles from each one, and stores them if they don't already exist in the database. It also adds tags to the articles. The scraping pauses randomly between requests to be polite and avoid getting blocked.

       Args:
           start_page (int): The first page to start scraping from.
           end_page (int): The last page to scrape.

       Returns:
           None
       """
    base_url = 'https://www.zoomit.ir/'
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
    for page_number in range(start_page, end_page + 1):
        url = f'https://api2.zoomit.ir/editorial/api/articles/browse?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber={page_number}&PageSize=20'
        response = requests.get(url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,'
                      'image/svg+xml,*/*;q=0.8'
        })
        print(response.status_code)
        if response.status_code != 200:
            print(f"could not feth page {page_number}")
        body_dict = response.json()
        count_articles_in_page = len(body_dict['source'])

        for i in range(count_articles_in_page):
            domain = body_dict['source'][i].get('slug')
            if domain is None:
                continue
            link = urljoin(base_url, domain)
            title, tags, writer, content, published_date = extract_article_data(link)

            if title is not None:
                # Create or update article in the database
                if title is not None:
                    # Check if the article already exists
                    article, created = Article.objects.get_or_create(
                        title=title,
                        url=link,
                        defaults={
                            'content': '\n'.join(content),  # Join content list into a single string
                            'author': writer,
                            'pub_date': published_date,
                        }
                    )

                    if created:
                        print(f"Article '{title}' created.")
                    else:
                        print(f"Article '{title}' already exists, skipping.")

                    for tag_name in tags:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        article.tags.add(tag)

        time.sleep(random.randint(1, 5))
