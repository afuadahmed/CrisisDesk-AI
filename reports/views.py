from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404, render
from django.db.models import Count

from .models import Report, ReportActivity
from .serializers import ReportSerializer
from .services.ai_service import classify_report
from .services.duplicate_service import detect_duplicate

class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    
class ReportListCreateView(APIView):

    def get(self, request):
        reports = Report.objects.all()

        category = request.query_params.get("category")
        urgency = request.query_params.get("urgency")
        report_status = request.query_params.get("status")
        ordering = request.query_params.get(
            "ordering",
            "-created_at"
        )

        if category:
            reports = reports.filter(category=category)

        if urgency:
            reports = reports.filter(urgency=urgency)

        if report_status:
            reports = reports.filter(status=report_status)

        allowed_ordering = [
            "created_at",
            "-created_at",
            "confidence",
            "-confidence",
        ]

        if ordering not in allowed_ordering:
            ordering = "-created_at"

        reports = reports.order_by(ordering)

        paginator = ReportPagination()
        page = paginator.paginate_queryset(
            reports,
            request,
            view=self
        )

        serializer = ReportSerializer(page, many=True)

        return paginator.get_paginated_response(
            {
                "success": True,
                "data": serializer.data,
            }
        )

    def post(self, request):
        serializer = ReportSerializer(data=request.data)

        if not serializer.is_valid():
            print("SERIALIZER ERRORS:", serializer.errors)
            return Response(
                {
                    "success": False,
                    "message": "Invalid report data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data

        try:
            ai_result = classify_report(
                description=validated_data["description"],
                location=validated_data["location"],
                language=validated_data.get("language", "unknown"),
            )
        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "AI classification failed. Please try again.",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        duplicate_result = detect_duplicate(
            description=validated_data["description"],
            location=validated_data["location"],
            category=ai_result["category"],
        )

        report = Report.objects.create(
            name=validated_data.get("name", ""),
            contact=validated_data.get("contact", ""),
            location=validated_data["location"],
            description=validated_data["description"],
            language=validated_data.get("language", "unknown"),
            category=ai_result["category"],
            urgency=ai_result["urgency"],
            summary=ai_result["summary"],
            suggested_action=ai_result["suggestedAction"],
            confidence=ai_result["confidence"],
            possible_duplicate=duplicate_result["possible_duplicate"],
            duplicate_similarity=duplicate_result["similarity_score"],
            matched_report=duplicate_result["matched_report"],
        )

        if report.possible_duplicate and report.matched_report:
            incident_root = (
                report.matched_report.incident
                or report.matched_report
            )

            report.incident = incident_root
        else:
            report.incident = report

        report.save(update_fields=["incident"])

        ReportActivity.objects.create(
            report=report,
            action="created",
            new_status=report.status,
        )

        response_serializer = ReportSerializer(report)

        return Response(
            {
                "success": True,
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    
class ReportDetailView(APIView):

    def get(self, request, report_id):
        report = get_object_or_404(
            Report,
            id=report_id
        )

        serializer = ReportSerializer(report)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ReportStatusUpdateView(APIView):

    def patch(self, request, report_id):
        report = get_object_or_404(
            Report,
            id=report_id
        )

        new_status = request.data.get("status")

        valid_statuses = [
            choice[0]
            for choice in Report.STATUS_CHOICES
        ]

        if new_status not in valid_statuses:
            return Response(
                {
                    "success": False,
                    "message": "Invalid report status.",
                    "validStatuses": valid_statuses,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = report.status

        report.status = new_status
        report.save(update_fields=["status", "updated_at"])

        if old_status != new_status:
            ReportActivity.objects.create(
                report=report,
                action="status_changed",
                old_status=old_status,
                new_status=new_status,
            )

        serializer = ReportSerializer(report)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
class AnalyticsSummaryView(APIView):

    def get(self, request):
        reports = Report.objects.all()

        total_reports = reports.count()

        critical_reports = reports.filter(
            urgency="critical"
        ).count()

        possible_duplicates = reports.filter(
            possible_duplicate=True
        ).count()

        category_counts = {
            item["category"]: item["count"]
            for item in reports.values("category").annotate(
                count=Count("id")
            )
        }

        status_counts = {
            item["status"]: item["count"]
            for item in reports.values("status").annotate(
                count=Count("id")
            )
        }

        urgency_counts = {
            item["urgency"]: item["count"]
            for item in reports.values("urgency").annotate(
                count=Count("id")
            )
        }

        return Response(
            {
                "success": True,
                "data": {
                    "totalReports": total_reports,
                    "criticalReports": critical_reports,
                    "possibleDuplicates": possible_duplicates,
                    "categories": category_counts,
                    "statuses": status_counts,
                    "urgencies": urgency_counts,
                },
            },
            status=status.HTTP_200_OK,
        )
def dashboard_view(request):
    return render(request, "dashboard.html")