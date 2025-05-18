from django.contrib import admin

from planetarium.models import (ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Ticket, Reservation)

admin.site.site_header = "Planetarium Administration"
admin.site.site_title = "Planetarium Administration"
admin.site.index_title = "Welcome to Planetarium Administration"
admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(PlanetariumDome)
admin.site.register(ShowSession)
admin.site.register(Ticket)
admin.site.register(Reservation)
