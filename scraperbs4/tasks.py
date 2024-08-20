from celery import shared_task
from .spider import scrape_zoomit


@shared_task
def run_scraper(from_page, to_page):
    scrape_zoomit(from_page, to_page)
