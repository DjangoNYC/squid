from django.contrib import admin
from .models import Member, Event, Venue, MemberRSVP


admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(MemberRSVP)
