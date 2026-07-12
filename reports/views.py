from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report
from .serializers import ReportSerializer
from .services.ai_service import classify_report
from .services.duplicate_service import detect_duplicate


class ReportListCreateView(APIView):

    def post(self, request):
        serializer = ReportSerializer(data=request.data)

        if not serializer.is_valid():
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
            matched_report=duplicate_result["matched_report"],
        )

        response_serializer = ReportSerializer(report)

        return Response(
            {
                "success": True,
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )