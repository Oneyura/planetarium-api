import datetime

from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, Reservation, Ticket, ShowSession
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import ShowThemeSerializer, AstronomyShowSerializer, PlanetariumDomeSerializer, \
    ReservationSerializer, ShowSessionSerializer, AstronomyShowListSerializer, ShowSessionListSerializer, \
    ReservationListSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("show_theme", "show_sessions")
    serializer_class = AstronomyShowSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AstronomyShowListSerializer
        return AstronomyShowSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")

        queryset = self.queryset
        if title:
            queryset = queryset.filter(Q(title__icontains=title) | Q(description__icontains=title) | Q(show_theme__name__icontains=title))
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Search by title of AstronomyShow, ShowTheme or show description.",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome").prefetch_related("tickets")
    serializer_class = ShowSessionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ShowSessionListSerializer
        return ShowSessionSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title")
        show_time = self.request.query_params.get("show_time")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(
                Q(astronomy_show__title__icontains=title) | Q(astronomy_show__description__icontains=title) | Q(astronomy_show__show_theme__name__icontains=title))

        if show_time:
            show_time = datetime.strptime(show_time, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time=show_time)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Search by title of AstronomyShow, ShowTheme or show description.",
            ),
            OpenApiParameter(
                "show_time",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by show_time of ShowSession "
                    "(ex. ?date=2022-10-23)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)





class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reservation.objects.select_related("tickets", "user", "show_session")
    serializer_class = ReservationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = ReservationPagination

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer
        return ReservationSerializer
