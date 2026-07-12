from rest_framework import serializers

from .models import Report, ReportActivity


class ReportActivitySerializer(serializers.ModelSerializer):
    actionDisplay = serializers.CharField(
        source="get_action_display",
        read_only=True,
    )

    oldStatus = serializers.CharField(
        source="old_status",
        read_only=True,
    )

    newStatus = serializers.CharField(
        source="new_status",
        read_only=True,
    )

    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True,
    )

    class Meta:
        model = ReportActivity
        fields = [
            "id",
            "action",
            "actionDisplay",
            "oldStatus",
            "newStatus",
            "createdAt",
        ]


class ReportSerializer(serializers.ModelSerializer):
    suggestedAction = serializers.CharField(
        source="suggested_action",
        read_only=True,
    )

    possibleDuplicate = serializers.BooleanField(
        source="possible_duplicate",
        read_only=True,
    )

    matchedReportId = serializers.UUIDField(
        source="matched_report_id",
        read_only=True,
        allow_null=True,
    )

    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True,
    )

    updatedAt = serializers.DateTimeField(
        source="updated_at",
        read_only=True,
    )

    activities = ReportActivitySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Report
        fields = "__all__"

        read_only_fields = [
            "id",
            "category",
            "urgency",
            "summary",
            "suggested_action",
            "confidence",
            "possible_duplicate",
            "duplicate_similarity",
            "matched_report",
            "status",
            "created_at",
            "updated_at",
        ]