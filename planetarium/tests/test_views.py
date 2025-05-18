import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import make_aware

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Reservation, Ticket
from users.models import User


class PlanetariumTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.theme = ShowTheme.objects.create(name="Cosmos")
        self.show = AstronomyShow.objects.create(title="Stars", description="A show about stars")
        self.show.show_theme.set([self.theme])

        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=10, seats_in_row=10)

        self.session = ShowSession.objects.create(
            show_time=make_aware(datetime.datetime(2025, 5, 18, 15, 0)),
            astronomy_show=self.show,
            planetarium_dome=self.dome
        )

    def test_create_show_theme(self):
        url = reverse("planetarium:showtheme-list")
        data = {"name": "Planets"}

        admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.client.force_authenticate(user=admin_user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 2)

    def test_list_astronomy_shows(self):
        url = reverse("planetarium:astronomyshow-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        results = response_data.get('results', response_data)
        self.assertTrue(any(show["title"] == "Stars" for show in results))

    def test_create_reservation(self):
        url = reverse("planetarium:reservation-list")
        data = {
            "tickets": [
                {"show_session": self.session.id, "row": 1, "seat": 1}
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_ticket_validation_invalid_seat(self):
        url = reverse("planetarium:reservation-list")
        data = {
            "tickets": [
                {"show_session": self.session.id, "row": 11, "seat": 1}
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("row", response.data["tickets"][0])

    def test_get_reservations(self):
        reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(show_session=self.session, reservation=reservation, row=1, seat=2)

        url = reverse("planetarium:reservation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
