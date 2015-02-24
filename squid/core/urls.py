from django.conf.urls import patterns, url
from .views import EventListView, EventDetailView, EventLandingView


urlpatterns = patterns('core.views',
    url(r'^$',
        EventLandingView.as_view(),
        name="event_landing"),
    url(r'^event/list/$',
        EventListView.as_view(),
        name="events"),
    url(r'^event/(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name="event_detail"),
)
