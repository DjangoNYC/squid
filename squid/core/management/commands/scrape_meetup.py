"""
This scrapes for Django NYC meetup data
"""
from django.core.management.base import BaseCommand
import requests
import json
from datetime import datetime
import pytz

from django.conf import settings

from core.models import Member, Event, Venue, MemberRSVP


class Command(BaseCommand):
    def handle(self, *args, **options):
        API_BASE = 'https://api.meetup.com/'

        def get_meetup_json(endpoint, **params):
            request_url = "{base}{endpoint}".format(
                base=API_BASE,
                endpoint=endpoint
                )

            api_params = {'sign': 'true',
                          'key': settings.MEETUP_API_KEY}
            # add custom request params
            request_params = dict(api_params.items() +
                                  params.items())

            request = requests.get(request_url, params=request_params)
            # FIXME: add some exception handling
            return json.loads(request.content)

        # Get all past events
        events_json = get_meetup_json('/2/events', group_urlname='django-nyc', status='past')

        """
        For each event:
        1. Get or create Event model
        2. Get or create event's location as Venue model
        3. Get or create each event attendees as Member model
        4. Get or create each event RSVP as MemberRSVP model
        """

        # 1. Get or create Event model
        # keep track of how many events created
        events_created = 0
        venues_created = 0
        members_created = 0
        rsvps_created = 0

        def add_created(counter, created):
            if created:
                counter += 1

        # FIXME: Add a while loop for 'next' in meta
        for record in events_json['results']:
            venue, new_venue = Venue.objects.get_or_create(
                meetup_id=record['venue']['id'],
                name=record['venue']['name'],
                longitude=record['venue']['lon'],
                latitude=record['venue']['lat']
                )
            add_created(venues_created, new_venue)

            # convert epoch time to datetime (UTC)
            # NOTE: meetup stores epoch time in milliseconds
            # FIXME: make timezone aware
            event_time = datetime.fromtimestamp(record['time']/1000)
            event, new_event = Event.objects.get_or_create(
                venue=venue,
                meetup_id=record['id'],
                meetup_url=record['event_url'],
                title=record['name'],
                date=event_time
                )

            add_created(events_created, new_event)

            rsvps_json = get_meetup_json('/2/rsvps', event_id=event.meetup_id)

            # FIXME: with proper exception handling
            if 'problem' in rsvps_json.keys():
                rsvps_json['results'] = list()

            for rsvp in rsvps_json['results']:
                member, new_member = Member.objects.get_or_create(
                    meetup_id=rsvp['member']['member_id'],
                    name=rsvp['member']['name']
                    )

                add_created(members_created, new_member)

                rsvp_time = datetime.fromtimestamp(rsvp['created']/1000)
                member_rsvp, new_rsvp = MemberRSVP.objects.get_or_create(
                    meetup_id=rsvp['rsvp_id'],
                    member=member,
                    event=event,
                    join_date=rsvp_time
                    )

                add_created(rsvps_created, new_rsvp)

        def print_update(model, retrieved, created):
            print("{retrieved} past {model} retrieved, {created} {model} created".format(
              retrieved=retrieved,
              model=model,
              created=created
              ))

        print_update('events', events_json['meta']['count'], events_created)
        print_update('venues', Venue.objects.all().count(), venues_created)
        print_update('members', Member.objects.all().count(), members_created)
        print_update('rsvps', MemberRSVP.objects.all().count(), rsvps_created)
