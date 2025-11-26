from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class BusinessProfile(models.Model):
    BUSINESS_TYPES = [
        ('retail', 'Retail'),
        ('service', 'Service'),
        ('food', 'Food & Beverage'),
        ('health', 'Health & Beauty'),
        ('tech', 'Technology'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    description = models.TextField()
    target_audience = models.JSONField(default=dict)  # Stores audience demographics
    location = models.CharField(max_length=255)
    contact_info = models.JSONField(default=dict)  # Phone, email, social media
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

class GrowthPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='growth_plans')
    weekly_plan = models.JSONField(default=dict)  # Structured weekly marketing plan
    messaging_tone = models.CharField(max_length=100)
    target_platforms = models.JSONField(default=list)  # ['facebook', 'instagram', etc.]
    daily_actions = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MarketingContent(models.Model):
    CONTENT_TYPES = [
        ('social_post', 'Social Media Post'),
        ('product_desc', 'Product Description'),
        ('ad_copy', 'Ad Copy'),
        ('video_script', 'Video Script'),
        ('email', 'Email Campaign'),
        ('whatsapp', 'WhatsApp Message'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='marketing_content')
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    platform = models.CharField(max_length=50, blank=True)
    content_text = models.TextField()
    metadata = models.JSONField(default=dict)  # Hashtags, tone, target audience
    is_approved = models.BooleanField(default=False)
    is_posted = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ContentGenerationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['ip_address', 'session_key']),
            models.Index(fields=['created_at']),
        ]