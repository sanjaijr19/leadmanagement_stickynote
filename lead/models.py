from django.db import models
import datetime
# Create your models here.
from django.db import models


class Lead_Source(models.Model):
    Lead_Source_name = models.CharField(max_length=30, blank=False, null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.Lead_Source_name


class Lead(models.Model):
    # other = models.ForeignKey(Lead_Source, on_delete=models.CASCADE)
    LEAD_SOURCE_CHOICES = (
        ('friend', 'friend'),
        ('family', 'family'),
        ('office', 'office'),
        ('other', 'other'),
        # Add more source choices as needed
    )

    LEAD_STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('converted', 'Converted'),
        # Add more status choices as needed
    )

    LEAD_SCORE_CHOICES = (
        ('25%', '25%'),
        ('50%', '50%'),
        ('75%', '75%'),
        ('100%', '100%'),
        # Add more score choices as needed
    )

    lead_name = models.CharField(max_length=30, blank=False, null=False)
    lead_image = models.ImageField(upload_to='lead_images/', null=True, blank=True)
    designation = models.CharField(max_length=30, blank=False, null=False)
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES)
    # lead_source = models.ForeignKey(Lead_Source, on_delete=models.CASCADE, related_name='lead_source')
    phone_number = models.BigIntegerField()
    email_id = models.EmailField()
    address = models.TextField()
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES)
    lead_score = models.CharField(max_length=10, choices=LEAD_SCORE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lead_name



