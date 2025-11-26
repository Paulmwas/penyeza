from django.urls import path
from . import views

urlpatterns = [
    path('business/profile/', views.BusinessProfileView.as_view(), name='business-profile'),
    path('business/growth-plan/', views.GrowthPlanView.as_view(), name='growth-plan'),
    path('content/generate/', views.generate_marketing_content, name='generate-content'),
    path('content/', views.MarketingContentView.as_view(), name='marketing-content'),
    path('content/<uuid:content_id>/approve/', views.approve_content, name='approve-content'),
]