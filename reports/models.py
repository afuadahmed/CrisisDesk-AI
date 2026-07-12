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

    matched_report = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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