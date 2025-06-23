from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = (
            "id",
            "name",
        )


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme",
        )


class AstronomyShowListSerializer(serializers.ModelSerializer):
    show_theme = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    show_sessions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="id",
    )

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme",
            "show_sessions",
        )


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
        )


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show",
            "planetarium_dome",
        )


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title",
    )
    planetarium_dome = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )
    show_theme = serializers.SlugRelatedField(
        source="astronomy_show.show_theme",
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show",
            "planetarium_dome",
            "show_theme",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["show_session"].planetarium_dome,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "show_session",
            "row",
            "seat",
        )


class TicketListSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer(many=False, read_only=True)
    user = SlugRelatedField(
        source="reservation.ser",
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Ticket
        fields = (
            "id",
            "show_session",
            "user",
            "row",
            "seat",
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "user",
            "created_at",
            "tickets",
        )
