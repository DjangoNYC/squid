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

        # keep track of how many events created
        created_counters = {
            'members': 0,
            'venues': 0,
            'rsvps': 0,
            'events': 0,
        }

        def add_created(counter_name, created):
            counter = created_counters[counter_name]
            if created:
                counter = counter + 1

        def save_member(member_json):
            joined = datetime.fromtimestamp(member_json['joined']/1000)
            if 'photo' in member_json.keys():
                photo_url = member_json['photo']['photo_link']
            else:
                photo_url = ''

            member, new_member = Member.objects.get_or_create(
                meetup_id=member_json['id'],
                name=member_json['name'],
                thumb_link=photo_url,
                join_date=joined
                )

            return new_member

        def process_events(events_json):
            # FIXME: Add a while loop for 'next' in meta
            for record in events_json['results']:
                """
                For each event:
                1. Get or create event's location as Venue model
                2. Get or create Event model
                3. Get or create each event attendees as Member model
                4. Get or create each event RSVP as MemberRSVP model
                """

                # 1. Get or create Venue model
                venue, new_venue = Venue.objects.get_or_create(
                    meetup_id=record['venue']['id'],
                    name=record['venue']['name'],
                    longitude=record['venue']['lon'],
                    latitude=record['venue']['lat']
                    )
                add_created('venues', new_venue)

                # 2. Get or create Event model
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
                add_created('events', new_event)

                rsvps_json = get_meetup_json('/2/rsvps', event_id=event.meetup_id)

                # FIXME: with proper exception handling
                if 'problem' in rsvps_json.keys():
                    rsvps_json['results'] = list()

                for rsvp in rsvps_json['results']:
                    member, new_member = Member.objects.get_or_create(
                        meetup_id=rsvp['member']['member_id'],
                        name=rsvp['member']['name']
                        )
                    add_created('members', new_member)

                    rsvp_time = datetime.fromtimestamp(rsvp['created']/1000)
                    member_rsvp, new_rsvp = MemberRSVP.objects.get_or_create(
                        meetup_id=rsvp['rsvp_id'],
                        member=member,
                        event=event,
                        join_date=rsvp_time
                        )

                    add_created('rsvps', new_rsvp)

        # Get all members
        # FIXME: Add while loop for next in meta logic 
        for offset in xrange(0, 8):
            members_json = get_meetup_json('/2/members', group_urlname='django-nyc', offset=offset)

            for member in members_json['results']:
                new_member = save_member(member)
                # FIXME: Something's up here
                # members_created = add_created(members_created, new_member)

        # Get all past events plus next upcoming event
        past_events_json = get_meetup_json('/2/events', group_urlname='django-nyc', status='past')
        process_events(past_events_json)
        upcoming_events_json = get_meetup_json('/2/events', group_urlname='django-nyc', status='upcoming', page='1')
        process_events(upcoming_events_json)

        def print_update(model, retrieved):
            print("{retrieved} past {model} retrieved, {created} {model} created".format(
              retrieved=retrieved,
              model=model,
              created=created_counters[model]
              ))

        print_update('events', Event.objects.all().count())
        print_update('venues', Venue.objects.all().count())
        print_update('members', Member.objects.all().count())
        print_update('rsvps', MemberRSVP.objects.all().count())
