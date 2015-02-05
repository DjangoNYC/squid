from django.db import models
from model_utils.models import TimeStampedModel


class Member(TimeStampedModel):
    """
    Django NYC member
    """
    meetup_id = models.PositiveIntegerField(max_length=32)
    name = models.CharField(max_length=128)
    photo = models.ImageField(null=True, blank=True)
    join_date = models.DateTimeField(null=True, blank=True)


class Event(TimeStampedModel):
    """
    Django NYC events
    """
    venue = models.ForeignKey('core.Venue', related_name="events")
    meetup_id = models.PositiveIntegerField(max_length=32)
    title = models.CharField(max_length=128)
    date = models.DateTimeField(null=True, blank=True)

    @property
    def rsvp_count(self):
        return self.rsvps.count()


class Venue(TimeStampedModel):
    meetup_id = models.PositiveIntegerField(max_length=32)
    name = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)
    latitude = models.CharField(max_length=128)


class MemberRSVP(TimeStampedModel):
    """
    Django NYC RSVPs to events by members
    """
    meetup_id = models.PositiveIntegerField(max_length=32)
    member = models.ForeignKey('core.Member', related_name="events")
    event = models.ForeignKey('core.Event', related_name="rsvps")
    join_date = models.DateTimeField(null=True, blank=True)
