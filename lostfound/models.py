from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class LostItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_lost = models.DateField(null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FoundItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_found = models.DateField(null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='found_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, null=True, blank=True, related_name='claims')
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, null=True, blank=True, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.pk} - {self.status}"