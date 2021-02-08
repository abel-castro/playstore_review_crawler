Playstore Review Crawler
========================

A celery task that runs every hour, gets app reviews from the Google Playstore and saves them in the database.


.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


Quick Start
-----------
Build the project and start the server:

    docker-compose -f local.yml up


The celery task **playstore_review_crawler.crawler.tasks.save_reviews_task** will run
every our and get the reviews for the app defined in the settings.


If you don't want to wait for the celery task, you can also run the task manually with this command:

    docker-compose -f local.yml run --rm django /app/manage.py save_app_reviews


Other Commands
--------------
Create a superuser:

    docker-compose -f local.yml run --rm django /app/manage.py createsuperuser


Run the tests:

    docker-compose -f local.yml run --rm django pytest


Settings
--------
In **config/settings/base.py** are defined the settings for the Crawler. Change them with your desired values.


Further settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html


