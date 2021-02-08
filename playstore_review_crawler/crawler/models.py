from django.db import models


class App(models.Model):
    app_id = models.CharField(max_length=100)

    def __str__(self):
        return self.app_id


class Review(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    review_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_image = models.URLField(max_length=255)
    content = models.TextField(null=True)
    score = models.PositiveIntegerField()
    thumbs_up_count = models.PositiveIntegerField()
    review_created_version = models.CharField(max_length=50, null=True)
    at = models.DateTimeField()
    reply_content = models.TextField(null=True)
    replied_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.app}: review id {self.id}"
