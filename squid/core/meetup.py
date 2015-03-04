import requests
import json
from datetime import datetime
import pytz

from django.conf import settings

from core.models import Member, Event, Venue, MemberRSVP


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


def save_member(member_json):
    joined = datetime.fromtimestamp(member_json['joined']/1000)
    # localize to UTC
    joined = pytz.timezone("UTC").localize(joined)
    if 'photo' in member_json.keys():
        photo_url = member_json['photo']['photo_link']
    else:
        photo_url = ''

    member, new_member = Member.objects.get_or_create(
        meetup_id=member_json['id'],
        name=member_json['name']
        )
    
    updated = False
    # allow for changes in photo url and join date
    if not photo_url == member.thumb_link:
        member.thumb_link = photo_url
        updated = True
    if not member.join_date == joined:
        member.join_date = joined
        updated = True

    if updated:
        member.save() 

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

        # 2. Get or create Event model
        # convert epoch time to datetime (UTC)
        # NOTE: meetup stores epoch time in milliseconds
        # FIXME: make timezone aware
        event_time = datetime.fromtimestamp(record['time']/1000)
        event_time = pytz.timezone("UTC").localize(event_time)
        event, new_event = Event.objects.get_or_create(
            venue=venue,
            meetup_id=record['id'],
            meetup_url=record['event_url'],
            title=record['name'],
            date=event_time
            )

        import ipdb; ipdb.set_trace()
        rsvps_json = get_meetup_json('/2/rsvps', event_id=event.meetup_id)

        # FIXME: with proper exception handling
        if 'problem' in rsvps_json.keys():
            rsvps_json['results'] = list()

        # filter only 'yes' responses
        rsvps_results = [r for r in rsvps_json['results'] if r['response'] == 'yes']

        for rsvp in rsvps_results:
            member, new_member = Member.objects.get_or_create(
                meetup_id=rsvp['member']['member_id'],
                name=rsvp['member']['name']
                )

            rsvp_time = datetime.fromtimestamp(rsvp['created']/1000)
            rsvp_time = pytz.timezone("UTC").localize(rsvp_time)
            member_rsvp, new_rsvp = MemberRSVP.objects.get_or_create(
                meetup_id=rsvp['rsvp_id'],
                member=member,
                event=event,
                join_date=rsvp_time
                )

