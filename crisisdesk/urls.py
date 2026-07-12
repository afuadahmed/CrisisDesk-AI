from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def dashboard_view(request):
    return render(request, "dashboard.html")


def report_view(request):
    return render(request, "report.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("reports.urls")),
    path("report/", report_view, name="report"),
    path("", dashboard_view, name="dashboard"),
]