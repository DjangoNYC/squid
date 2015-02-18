from django.conf.urls import patterns, url
from .views import EventListView, EventDetailView


urlpatterns = patterns('core.views',
    url(r'^$',
        EventListView.as_view(),
        name="events"),
    url(r'^event/(?P<pk>\d+)$',
        EventDetailView.as_view(),
        name="event_detail"),
)
