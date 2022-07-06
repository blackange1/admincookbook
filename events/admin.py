from django.contrib import admin

from .models import Epic, Event, EventHero, EventVillain


# create two independent admin sites
class EventAdminSite(admin.AdminSite):
    site_header = "UMSRA Events Admin"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"


event_admin_site = EventAdminSite(name='event_admin')

event_admin_site.register(Epic)
event_admin_site.register(Event)
event_admin_site.register(EventHero)
event_admin_site.register(EventVillain)
