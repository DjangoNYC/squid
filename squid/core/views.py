# Create your views here.
from decimal import *

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings

from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import Member, Event, Venue, MemberRSVP

class MemberView(ListView):
	model = Member
	template_name = "members.html"


class EventListView(ListView):
	model = Event
	template_name = "events.html"


class EventDetailView(DetailView):
	model = Event
	template_name = "event_detail.html"


class VenueView(ListView):
	model = Venue
	template_name = "venues.html"


class MemberRSVPView(ListView):
	model = MemberRSVP
	template_name = "rsvps.html"
