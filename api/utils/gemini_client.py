import google.generativeai as genai
import os
import json
from django.conf import settings
from typing import Dict, List, Optional

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in settings")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_marketing_content(self, business_context: Dict, content_type: str, platform: str) -> Dict:
        prompt = self._build_prompt(business_context, content_type, platform)
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'content': response.text.strip(),
                'type': content_type,
                'platform': platform
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def _build_prompt(self, business_context: Dict, content_type: str, platform: str) -> str:
        base_prompt = f"""
        You are Penyeza AI Growth Agent, an expert marketing assistant for small businesses in Africa.
        
        BUSINESS CONTEXT:
        - Business Name: {business_context.get('business_name', 'Local Business')}
        - Business Type: {business_context.get('business_type', 'General')}
        - Description: {business_context.get('description', 'Serving local community')}
        - Target Audience: {business_context.get('target_audience', 'Local customers')}
        - Location: {business_context.get('location', 'Local area')}
        
        TASK: Create a {content_type.upper()} for {platform.upper()}
        
        REQUIREMENTS:
        - Engaging and professional tone
        - Culturally appropriate for African markets
        - Action-oriented with clear call-to-action
        - Optimized for the specific platform
        - Includes relevant local context
        - Mobile-friendly format
        
        ADDITIONAL CONTEXT:
        {business_context.get('platform_specific', 'Create compelling content that drives engagement and sales.')}
        
        FORMAT: Provide only the final content, ready to use. No explanations or notes.
        """
        return base_prompt

    def generate_growth_plan(self, business_profile_data: Dict) -> Dict:
        prompt = f"""
        Create a comprehensive weekly marketing growth plan for this African small business:
        
        BUSINESS DETAILS:
        - Name: {business_profile_data.get('business_name')}
        - Type: {business_profile_data.get('business_type')}
        - Description: {business_profile_data.get('description')}
        - Target Audience: {business_profile_data.get('target_audience')}
        - Location: {business_profile_data.get('location')}
        
        Create a 7-day marketing plan with:
        
        DAY-BY-DAY ACTIVITIES:
        - Monday: Content theme and specific actions
        - Tuesday: Engagement strategies
        - Wednesday: Promotional activities
        - Thursday: Customer retention focus
        - Friday: Weekend preparation
        - Saturday: Peak engagement
        - Sunday: Planning and analysis
        
        PLATFORM STRATEGY:
        - Primary platforms to focus on
        - Content types for each platform
        - Best posting times
        
        PERFORMANCE METRICS:
        - Key metrics to track
        - Goals for the week
        - Success indicators
        
        Format the response as structured JSON that can be parsed.
        Focus on practical, actionable steps for African small businesses.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse JSON, if fails return as text
            try:
                plan_data = json.loads(response.text)
                return {'success': True, 'plan': plan_data}
            except:
                return {'success': True, 'plan': response.text}
        except Exception as e:
            return {'success': False, 'error': str(e)}