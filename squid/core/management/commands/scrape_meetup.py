"""
This scrapes for Django NYC meetup data
"""
from django.core.management.base import BaseCommand

from core.meetup import get_meetup_json, save_member, process_events


class Command(BaseCommand):
    def handle(self, *args, **options):
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
