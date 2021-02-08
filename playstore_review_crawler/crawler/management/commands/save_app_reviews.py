from django.core.management.base import BaseCommand
from playstore_review_crawler.crawler.crawler import Crawler

from config.settings.base import (
    APP_ID,
    AMOUNT_REVIEWS_TO_SAVE,
    REVIEWS_LANGUAGE,
    REVIEWS_COUNTRY,
)


class Command(BaseCommand):
    help = "Stores app reviews in the database."

    def handle(self, *args, **options):
        crawler = Crawler(app_id=APP_ID)
        crawler.save_reviews(
            amount=AMOUNT_REVIEWS_TO_SAVE,
            language=REVIEWS_LANGUAGE,
            country=REVIEWS_COUNTRY,
        )
