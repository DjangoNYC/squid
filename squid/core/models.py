from django.db import models
from model_utils.models import TimeStampedModel


class Member(TimeStampedModel):
    """
    Django NYC member
    """
    meetup_id = models.PositiveIntegerField(max_length=32)


class Event(TimeStampedModel):
    """
    Django NYC events
    """
    meetup_id = models.PositiveIntegerField(max_length=32)


class MemberRSVP(TimeStampedModel):
    """
    Django NYC RSVPs to events by members
    """
    meetup_id = models.PositiveIntegerField(max_length=32)
    member = models.ForeignKey('core.Member', related_name="events")
    event = models.ForeignKey('core.Event', related_name="rsvps")
