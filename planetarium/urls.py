from django.urls import path, include
from rest_framework.routers import DefaultRouter

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
)

router = DefaultRouter()
router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("show_sessions", ShowSessionViewSet, basename="show_session")
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "planetarium"
