from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Frontend pages
    path(
        "",
        TemplateView.as_view(template_name="dashboard.html"),
        name="dashboard",
    ),
    path(
        "report/",
        TemplateView.as_view(template_name="report.html"),
        name="report-crisis",
    ),

    # API
    path("api/", include("reports.urls")),

    # OpenAPI schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]