from django.urls import path

from .views import (
    ReportDetailView,
    ReportListCreateView,
    ReportStatusUpdateView,
)


urlpatterns = [
    path(
        "reports",
        ReportListCreateView.as_view(),
        name="report-list-create",
    ),
    path(
        "reports/<uuid:report_id>",
        ReportDetailView.as_view(),
        name="report-detail",
    ),
    path(
        "reports/<uuid:report_id>/status",
        ReportStatusUpdateView.as_view(),
        name="report-status-update",
    ),
]