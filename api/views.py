from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import BusinessProfile, GrowthPlan, MarketingContent
from .serializers import (
    BusinessProfileSerializer, GrowthPlanSerializer, 
    MarketingContentSerializer, ContentGenerationRequestSerializer
)
from .permissions import FreeTierRateLimit
from .utils.gemini_client import GeminiClient
import json

class BusinessProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = BusinessProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

class GrowthPlanView(generics.RetrieveAPIView):
    serializer_class = GrowthPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        business_profile = BusinessProfile.objects.get(user=self.request.user)
        plan, created = GrowthPlan.objects.get_or_create(
            business=business_profile,
            is_active=True
        )
        
        if created:
            # Generate initial growth plan using AI
            gemini = GeminiClient()
            plan_data = gemini.generate_growth_plan({
                'business_name': business_profile.business_name,
                'business_type': business_profile.business_type,
                'description': business_profile.description,
                'target_audience': business_profile.target_audience,
                'location': business_profile.location
            })
            
            if plan_data['success']:
                plan.weekly_plan = self._parse_ai_plan(plan_data['plan'])
                plan.messaging_tone = 'friendly_professional'
                plan.target_platforms = ['facebook', 'instagram', 'whatsapp']
                plan.save()
        
        return plan
    
    def _parse_ai_plan(self, ai_response):
        # Parse AI response into structured JSON
        try:
            return json.loads(ai_response)
        except:
            # Fallback structure if parsing fails
            return {
                "weekly_themes": ["Engagement", "Promotion", "Testimonials", "Education", "Community"],
                "daily_actions": [],
                "platforms": ["facebook", "instagram"]
            }

@api_view(['POST'])
@permission_classes([FreeTierRateLimit])
def generate_marketing_content(request):
    serializer = ContentGenerationRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get business context for authenticated users
    business_context = {}
    if request.user.is_authenticated:
        try:
            business_profile = BusinessProfile.objects.get(user=request.user)
            business_context = {
                'business_name': business_profile.business_name,
                'business_type': business_profile.business_type,
                'description': business_profile.description,
                'target_audience': business_profile.target_audience,
                'location': business_profile.location
            }
        except BusinessProfile.DoesNotExist:
            pass
    
    # Use default context for unauthenticated users
    if not business_context:
        business_context = {
            'business_name': 'Small Business',
            'business_type': 'general',
            'description': 'Local business serving the community',
            'target_audience': 'local customers',
            'location': 'your area'
        }
    
    # Generate content using Gemini AI
    gemini = GeminiClient()
    result = gemini.generate_marketing_content(
        business_context,
        serializer.validated_data['content_type'],
        serializer.validated_data.get('platform', 'general')
    )
    
    if result['success']:
        # Save content for authenticated users
        if request.user.is_authenticated:
            try:
                business_profile = BusinessProfile.objects.get(user=request.user)
                content = MarketingContent.objects.create(
                    business=business_profile,
                    content_type=serializer.validated_data['content_type'],
                    platform=serializer.validated_data.get('platform', ''),
                    content_text=result['content'],
                    metadata={
                        'tone': serializer.validated_data.get('tone', 'professional'),
                        'theme': serializer.validated_data.get('theme', ''),
                        'generated_at': timezone.now().isoformat()
                    }
                )
                result['content_id'] = str(content.id)
            except BusinessProfile.DoesNotExist:
                pass
        
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Failed to generate content', 'details': result['error']},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class MarketingContentView(generics.ListCreateAPIView):
    serializer_class = MarketingContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        business_profile = BusinessProfile.objects.get(user=self.request.user)
        return MarketingContent.objects.filter(business=business_profile).order_by('-created_at')
    
    def perform_create(self, serializer):
        business_profile = BusinessProfile.objects.get(user=self.request.user)
        serializer.save(business=business_profile)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_content(request, content_id):
    try:
        business_profile = BusinessProfile.objects.get(user=request.user)
        content = MarketingContent.objects.get(id=content_id, business=business_profile)
        content.is_approved = True
        content.save()
        return Response({'status': 'content approved'})
    except MarketingContent.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)