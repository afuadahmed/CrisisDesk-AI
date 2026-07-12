from django.urls import path

from .views import ReportListCreateView


urlpatterns = [
    path(
        "reports",
        ReportListCreateView.as_view(),
        name="report-list-create",
    ),
]