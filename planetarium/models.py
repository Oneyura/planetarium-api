from django.db import models
from django.db.models import ForeignKey, DateTimeField, ManyToManyField
from rest_framework.exceptions import ValidationError

from users.models import User


class ShowTheme(models.Model):
    name = models.CharField(max_length=100)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    show_theme = ManyToManyField(ShowTheme, related_name='astronomy_shows')


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ShowSession(models.Model):
    show_time = DateTimeField()
    astronomy_show = ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name='show_sessions')
    planetarium_dome = ForeignKey(PlanetariumDome, on_delete=models.CASCADE, related_name='show_sessions')


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']


class Ticket(models.Model):
    show_session = ForeignKey(ShowSession, on_delete=models.CASCADE, related_name='tickets')
    reservation = ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')
    row = models.IntegerField()
    seat = models.IntegerField()

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for ticket_attr_value, ticket_attr_name, planetarium_dome_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, planetarium_dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {planetarium_dome_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.reservation.user.email} - {self.row} - {self.seat}"

    class Meta:
        ordering = ['row', 'seat']
