import datetime
import pytest
from unittest.mock import patch


from .models import App, Review
from .crawler import Crawler
from .utils import make_aware_if_is_not_none

REVIEW_1 = {
    "reviewId": "gp:AOqpTOEidjUkkpl06U42OK2uF7h222BNlSbq0TOXYqNIH8PH83jrOPdgYR2z6dGwUIn3jHnEsqPTdAl8SH50Q3o",
    "userName": "Estelle Mageean",
    "userImage": "https://play-lh.googleusercontent.com/a-/AOh14Gjck72h2efuxGjY721qowxO9eXH_em2kTOQ7mmk5Q",
    "content": "Brilliant app. I like that I can predict the score and take part in quizzes and competitions. All the up to date news and activities. Love it!",
    "score": 5,
    "thumbsUpCount": 4,
    "reviewCreatedVersion": "6.0.0.2944",
    "at": datetime.datetime(2021, 2, 2, 12, 34, 57),
    "replyContent": None,
    "repliedAt": None,
}

REVIEW_2 = {
    "reviewId": "gp:AOqpTOEK73LyOk2WzqEob8onFXu2G8HnydvPzG87bZ-97uiXHRv_eaFM-mHkJLMPL-01rUgPLMIB5nYi7zc9PGU",
    "userName": "John Gotti Uchiha",
    "userImage": "https://play-lh.googleusercontent.com/a-/AOh14Ghu3sfiGW87UD_wFSAJjY_W7YQIi-GiOR_oDnjkKw",
    "content": "The only issue I got is that I been trying to change the language from English to Spanish and I don't see any options and everything the videos, Games is in English and I don't like it. I know you can change it in the website but I mostly use my phone app.",
    "score": 5,
    "thumbsUpCount": 114,
    "reviewCreatedVersion": "6.0.0.2876",
    "at": datetime.datetime(2020, 12, 2, 13, 58, 37),
    "replyContent": None,
    "repliedAt": None,
}

REVIEW_3 = {
    "reviewId": "gp:AOqpTOGe4ImHSajq5fdBpDB0BkgkM0n9d1lTGPkI5QtLahNIz9lmWDlGw2lrGQVMTG0wy6aHXMFuDGFLK0RHviw",
    "userName": "Benyamin SA",
    "userImage": "https://play-lh.googleusercontent.com/-5HlxkBw69FU/AAAAAAAAAAI/AAAAAAAAAAA/AMZuucnOd-cdXhUW911mRXYZunqwv-iIVQ/photo.jpg",
    "content": "The best app for Barca fans and a barca fan needs a one of I love barca for everytime;that is the best of teams all times Forca barca . Forca catalonya❤💙❤💙",
    "score": 5,
    "thumbsUpCount": 6,
    "reviewCreatedVersion": "6.0.0.2916",
    "at": datetime.datetime(2020, 12, 31, 20, 51, 35),
    "replyContent": None,
    "repliedAt": None,
}


REVIEW_DATA = [REVIEW_1, REVIEW_2, REVIEW_3]

TEST_APP_ID = "com.mcentric.mcclient.FCBWorld"


def mocked_get_reviews(*args, **kwargs):
    return REVIEW_DATA


@pytest.mark.django_db
def test__save_reviews__review_data():
    with patch.object(Crawler, "get_reviews", new=mocked_get_reviews):
        crawler = Crawler(app_id=TEST_APP_ID)
        crawler.save_reviews(amount=3)

        assert App.objects.count() == 1
        app = App.objects.get()
        assert app.app_id == TEST_APP_ID

        assert Review.objects.count() == 3
        review = Review.objects.first()
        assert review.review_id == REVIEW_DATA[0]["reviewId"]
        assert review.user_name == REVIEW_DATA[0]["userName"]
        assert review.user_image == REVIEW_DATA[0]["userImage"]
        assert review.content == REVIEW_DATA[0]["content"]
        assert review.score == REVIEW_DATA[0]["score"]
        assert review.thumbs_up_count == REVIEW_DATA[0]["thumbsUpCount"]
        assert review.review_created_version == REVIEW_DATA[0]["reviewCreatedVersion"]
        assert review.at == make_aware_if_is_not_none(REVIEW_DATA[0]["at"])
        assert review.reply_content == REVIEW_DATA[0]["replyContent"]
        assert review.replied_at == make_aware_if_is_not_none(
            REVIEW_DATA[0]["repliedAt"]
        )


@pytest.mark.django_db
def test__save_reviews__reviews_cleared_with_new_import():
    with patch.object(Crawler, "get_reviews", new=mocked_get_reviews):
        crawler = Crawler(app_id=TEST_APP_ID)
        crawler.save_reviews(3)

        assert Review.objects.count() == 3

        crawler = Crawler(app_id=TEST_APP_ID)
        crawler.save_reviews(3)

        assert Review.objects.count() == 3
