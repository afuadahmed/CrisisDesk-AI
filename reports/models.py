from django.db import models
import uuid


class Report(models.Model):

    CATEGORY_CHOICES = [
        ('medical', 'Medical'),
        ('fire', 'Fire'),
        ('accident', 'Accident'),
        ('crime', 'Crime'),
        ('flood', 'Flood'),
        ('utility', 'Utility'),
        ('public_service', 'Public Service'),
        ('infrastructure', 'Infrastructure'),
        ('other', 'Other'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    LANGUAGE_CHOICES = [
        ('bn', 'Bangla'),
        ('en', 'English'),
        ('unknown', 'Unknown'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('assigned', 'Assigned'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        blank=True
    )

    contact = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=255
    )

    description = models.TextField()

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='unknown'
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES
    )

    summary = models.TextField()

    suggested_action = models.TextField()

    confidence = models.FloatField()

    possible_duplicate = models.BooleanField(
        default=False
    )

    duplicate_similarity = models.FloatField(
    null=True,
    blank=True
)

    matched_report = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    incident = models.ForeignKey(
    "self",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="incident_reports"
)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.category} - {self.location}"
    
class ReportActivity(models.Model):

    ACTION_CHOICES = [
        ('created', 'Report Created'),
        ('status_changed', 'Status Changed'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    old_status = models.CharField(
        max_length=20,
        blank=True
    )

    new_status = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.report.id} - {self.action}"