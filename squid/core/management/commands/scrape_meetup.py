"""
This scrapes for Django NYC meetup data
"""
from django.core.management.base import BaseCommand
import requests

from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
        API_BASE = 'https://api.meetup.com/'

        def get_api_url(endpoint):
            return "{base}{endpoint}".format(
                base=API_BASE,
                endpoint=endpoint
                )

        api_key = settings.MEETUP_API_KEY
        api_params = {'sign':'true', 'key':api_key}

        group_params = api_params
        group_params['group_urlname'] = 'django-nyc'
        group_url = get_api_url('2/groups')

        django_nyc = requests.get(group_url, params=group_params)


