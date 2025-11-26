from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from .models import ContentGenerationRequest

class FreeTierRateLimit(permissions.BasePermission):
    """
    Allow 2 free content generations per IP/session, then require authentication
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
            
        # Check free tier usage
        ip = request.META.get('REMOTE_ADDR')
        session_key = request.session.session_key
        
        # Count requests in last 24 hours
        yesterday = timezone.now() - timedelta(hours=24)
        request_count = ContentGenerationRequest.objects.filter(
            ip_address=ip,
            created_at__gte=yesterday
        ).count()
        
        if request_count >= 2:
            return False
            
        # Log this request
        ContentGenerationRequest.objects.create(
            ip_address=ip,
            session_key=session_key or ''
        )
        return True