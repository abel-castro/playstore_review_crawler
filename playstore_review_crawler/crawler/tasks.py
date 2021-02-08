from config.celery_app import app
from config.settings.base import (
    APP_ID,
    AMOUNT_REVIEWS_TO_SAVE,
    REVIEWS_LANGUAGE,
    REVIEWS_COUNTRY,
)

from .crawler import Crawler


@app.task
def save_reviews_task():
    crawler = Crawler(app_id=APP_ID)
    crawler.save_reviews(
        amount=AMOUNT_REVIEWS_TO_SAVE,
        language=REVIEWS_LANGUAGE,
        country=REVIEWS_COUNTRY,
    )
