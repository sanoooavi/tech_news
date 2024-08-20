from bs4 import BeautifulSoup
import requests
import time
import random
from urllib.parse import urljoin
from datetime import datetime
from news.models import Article, Tag, ArticleTag


def get_month_number(month):
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
    base_url = 'https://www.zoomit.ir/'
    for page_number in range(start_page, end_page + 1):
        url = f'https://api2.zoomit.ir/editorial/api/articles/browse?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber={page_number}&PageSize=20'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"could not feth page {page_number}")
        body_dict = response.json()
        count_articles_in_page = len(body_dict['source'])

        for i in range(count_articles_in_page):
            domain = body_dict['source'][i]['slug']
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
                        ArticleTag.objects.get_or_create(article=article, tag=tag)

        time.sleep(random.randint(1, 5))
