# Create your views here.
from decimal import *

from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings

from django.core.urlresolvers import reverse
from django.shortcuts import render

from django.views.generic import ListView, DetailView, UpdateView, RedirectView

from django.shortcuts import get_object_or_404

from .models import Member, Event, Venue, MemberRSVP
from .forms import EventAttendeeForm


class MemberView(ListView):
    model = Member
    template_name = "members.html"
    

class EventListView(ListView):
    model = Event
    template_name = "events.html"


class EventLandingView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        latest_event = Event.objects.latest('date') 
        return reverse('event_detail', kwargs={'pk': latest_event.id})

        
class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        event = self.get_object()
        # build rsvp form list 
        rsvp_list = [EventAttendeeForm(instance=rsvp) for rsvp in event.rsvps.all().order_by('member__name')]
        context['rsvp_list'] = rsvp_list
        return context

    def get_success_url(self):
        event = self.get_object()
        return reverse('event_detail', kwargs={'pk': event.id})

    def post(self, request, *args, **kwargs):
        rsvp = get_object_or_404(MemberRSVP, pk=request.POST['id'])
        form = EventAttendeeForm(data=request.POST, instance=rsvp)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.get_success_url())
            
class VenueView(ListView):
    model = Venue
    template_name = "venues.html"


class MemberRSVPView(ListView):
    model = MemberRSVP
    template_name = "rsvps.html"
