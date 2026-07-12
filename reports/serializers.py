from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):

    suggestedAction = serializers.CharField(
        source='suggested_action',
        read_only=True
    )

    possibleDuplicate = serializers.BooleanField(
        source='possible_duplicate',
        read_only=True
    )

    matchedReportId = serializers.UUIDField(
        source='matched_report.id',
        read_only=True,
        allow_null=True
    )

    createdAt = serializers.DateTimeField(
        source='created_at',
        read_only=True
    )

    updatedAt = serializers.DateTimeField(
        source='updated_at',
        read_only=True
    )

    class Meta:
        model = Report

        fields = [
            'id',
            'name',
            'contact',
            'location',
            'description',
            'language',
            'category',
            'urgency',
            'summary',
            'suggestedAction',
            'confidence',
            'possibleDuplicate',
            'matchedReportId',
            'status',
            'createdAt',
            'updatedAt',
        ]

        read_only_fields = [
            'id',
            'category',
            'urgency',
            'summary',
            'confidence',
            'status',
        ]

    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Description is required and cannot be empty."
            )

        return value.strip()

    def validate_location(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Location is required and cannot be empty."
            )

        return value.strip()