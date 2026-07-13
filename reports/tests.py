from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Report


class CrisisDeskAPITests(APITestCase):

    def setUp(self):
        self.report = Report.objects.create(
            name="Karim",
            contact="01800000000",
            location="Dhaka Mirpur 10",
            description=(
                "A bus overturned near Mirpur 10 "
                "and several passengers are injured."
            ),
            language="en",
            category="accident",
            urgency="critical",
            summary="Bus accident with multiple injuries.",
            suggested_action="Dispatch emergency medical services.",
            confidence=0.95,
        )

        self.report.incident = self.report
        self.report.save(update_fields=["incident"])

    def test_report_list_returns_success(self):
        response = self.client.get(
            reverse("report-list-create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["results"]["success"]
        )

    def test_report_detail_returns_report(self):
        response = self.client.get(
            reverse(
                "report-detail",
                kwargs={
                    "report_id": self.report.id
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["id"],
            str(self.report.id),
        )

    def test_report_search_filter(self):
        response = self.client.get(
            reverse("report-list-create"),
            {
                "search": "mirpur",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_report_status_update(self):
        response = self.client.patch(
            reverse(
                "report-status-update",
                kwargs={
                    "report_id": self.report.id
                },
            ),
            {
                "status": "assigned",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "assigned",
        )

    def test_incident_status_update(self):
        response = self.client.patch(
            reverse(
                "incident-status-update",
                kwargs={
                    "incident_id": self.report.id
                },
            ),
            {
                "status": "resolved",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "resolved",
        )

    def test_analytics_summary(self):
        response = self.client.get(
            reverse("report-stats-summary")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["data"]["totalReports"],
            1,
        )

    def test_invalid_status_is_rejected(self):
        response = self.client.patch(
            reverse(
                "report-status-update",
                kwargs={
                    "report_id": self.report.id
                },
            ),
            {
                "status": "invalid_status",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )