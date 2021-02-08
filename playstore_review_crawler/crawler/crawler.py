import logging
from django.utils.timezone import make_aware

from .utils import make_aware_if_is_not_none

from google_play_scraper import Sort
from google_play_scraper import reviews as get_google_playstore_reviews
from .models import App, Review
from config.settings.base import (
    AMOUNT_REVIEWS_TO_SAVE,
    REVIEWS_COUNTRY,
    REVIEWS_LANGUAGE,
)

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self, app_id):
        self.app_id = app_id
        self.amount_reviews_saved = 0

    def clear_app_reviews(self):
        """
        Delete all existing reviews for the passed app.
        """
        Review.objects.filter(app__app_id=self.app_id).delete()
        logger.info(f"Reviews for {self.app_id} cleared from the DB.")

    def get_reviews(self, *args, **kwargs) -> list:
        """
        Return a list reviews for the passed app_id.
        """
        amount = kwargs.get("amount", 0)
        language = kwargs.get("language")
        country = kwargs.get("country")
        reviews, continuation_token = get_google_playstore_reviews(
            self.app_id,
            lang=language,
            country=country,
            sort=Sort.MOST_RELEVANT,
            count=amount,
            filter_score_with=None,  # no filters
        )

        # if more than 3 reviews are required is necessary to use the continuation_token
        # for loading more results
        if amount > 3:
            reviews, _ = get_google_playstore_reviews(
                self.app_id,
                continuation_token=continuation_token,  # defaults to None(load from the beginning)
            )

        return reviews

    def save_reviews(
        self,
        amount: int = AMOUNT_REVIEWS_TO_SAVE,
        language: str = REVIEWS_LANGUAGE,
        country: str = REVIEWS_COUNTRY,
    ):
        """
        Save the reviews in the database.

        Before the reviews will be saved, all existing reviews for the passed
        app_id will be deleted.
        """
        reviews = self.get_reviews(amount=amount, language=language, country=country)

        if not reviews:
            logger.info(f"0 reviews found for the app {self.app_id}.")
            return

        self.clear_app_reviews()
        app, app_created = App.objects.get_or_create(app_id=self.app_id)

        for review in reviews:
            self.amount_reviews_saved += 1

            Review.objects.create(
                app=app,
                review_id=review["reviewId"],
                user_name=review["userName"],
                user_image=review.get("userImage"),
                content=review.get("content", ""),
                score=review["score"],
                thumbs_up_count=review["thumbsUpCount"],
                review_created_version=review["reviewCreatedVersion"],
                at=make_aware(review["at"]),
                reply_content=review.get("replyContent", None),
                replied_at=make_aware_if_is_not_none(review.get("repliedAt", None)),
            )
        logger.info(f"{self.amount_reviews_saved} reviews saved in the DB.")
