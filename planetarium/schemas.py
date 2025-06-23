from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

# AstronomyShowViewSet schema parameters
astronomy_show_list_params = [
    OpenApiParameter(
        "title",
        type=OpenApiTypes.STR,
        description="Search by title of AstronomyShow, ShowTheme or show description.",
    ),
]

# ShowSessionViewSet schema parameters
show_session_list_params = [
    OpenApiParameter(
        "title",
        type=OpenApiTypes.STR,
        description="Search by title of AstronomyShow, ShowTheme or show description.",
    ),
    OpenApiParameter(
        "show_time",
        type=OpenApiTypes.DATE,
        description="Filter by show_time of ShowSession (ex. ?date=2022-10-23)",
    ),
]