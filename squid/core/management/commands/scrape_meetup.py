"""
This scrapes for Django NYC meetup data
"""
from django.core.management.base import BaseCommand
import requests

from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
        api_key = settings.MEETUP_API_KEY
        api_params = {'sign':'true', 'key':api_key}

        group_params = api_params
        group_params['group_urlname'] = 'django-nyc'

        django_nyc = requests.get('https://api.meetup.com/2/groups', group_params)
