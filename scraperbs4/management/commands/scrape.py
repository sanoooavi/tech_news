from django.core.management.base import BaseCommand
from scraperbs4 import spider


class Command(BaseCommand):
    help = 'Runs the web scraper for a range of pages'

    def add_arguments(self, parser):
        # Define the integer arguments for the range of pages
        parser.add_argument('from_page', type=int, help='The starting page number')
        parser.add_argument('to_page', type=int, help='The ending page number')

    def handle(self, *args, **kwargs):
        from_page = kwargs['from_page']  # Get the starting page number
        to_page = kwargs['to_page']  # Get the ending page number

        # Call your scraper function with the provided range
        spider.scrape_zoomit(from_page, to_page)

        self.stdout.write(self.style.SUCCESS(f'Scraping completed from page {from_page} to {to_page}'))
