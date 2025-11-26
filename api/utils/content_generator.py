import json
import re
from typing import Dict, List, Optional
from .gemini_client import GeminiClient

class ContentGenerator:
    def __init__(self):
        self.gemini = GeminiClient()
    
    def generate_social_media_post(self, business_context: Dict, platform: str, theme: str = "") -> Dict:
        """Generate social media post with platform-specific formatting"""
        content_type = "social_post"
        
        # Platform-specific enhancements
        platform_prompts = {
            'facebook': "Create a Facebook post that encourages engagement (likes, comments, shares). Include a call-to-action.",
            'instagram': "Create an Instagram post with engaging captions and relevant hashtags. Make it visual and story-oriented.",
            'tiktok': "Create a TikTok video script with trending elements, hooks, and short engaging content.",
            'twitter': "Create a Twitter post that's concise, uses hashtags, and encourages retweets.",
            'whatsapp': "Create a WhatsApp broadcast message that's personal, direct, and encourages replies.",
            'linkedin': "Create a professional LinkedIn post that showcases business expertise and industry insights."
        }
        
        prompt_enhancement = platform_prompts.get(platform.lower(), "Create an engaging social media post.")
        
        if theme:
            prompt_enhancement += f" Theme: {theme}"
        
        business_context['platform_specific'] = prompt_enhancement
        
        result = self.gemini.generate_marketing_content(business_context, content_type, platform)
        
        if result['success']:
            # Enhance the content with structured data
            enhanced_content = self._enhance_social_content(result['content'], platform, theme)
            result['enhanced_content'] = enhanced_content
        return result
    
    def generate_product_description(self, business_context: Dict, product_details: Dict) -> Dict:
        """Generate compelling product descriptions"""
        content_type = "product_desc"
        
        # Add product details to business context
        enhanced_context = business_context.copy()
        enhanced_context['product_name'] = product_details.get('name', '')
        enhanced_context['product_features'] = product_details.get('features', [])
        enhanced_context['product_benefits'] = product_details.get('benefits', [])
        enhanced_context['target_customer'] = product_details.get('target_customer', '')
        
        result = self.gemini.generate_marketing_content(enhanced_context, content_type, 'general')
        
        if result['success']:
            # Structure the product description
            structured_description = self._structure_product_description(result['content'], product_details)
            result['structured_description'] = structured_description
        
        return result
    
    def generate_ad_copy(self, business_context: Dict, ad_type: str, promotion: Dict = None) -> Dict:
        """Generate advertising copy for various platforms"""
        content_type = "ad_copy"
        
        ad_type_prompts = {
            'sales': "Create compelling sales ad copy with strong call-to-action and urgency.",
            'awareness': "Create brand awareness ad copy that highlights unique value proposition.",
            'promotional': "Create promotional ad copy for special offers or discounts.",
            'lead_generation': "Create ad copy designed to generate leads and collect customer information.",
            'retargeting': "Create retargeting ad copy for customers who have shown interest before."
        }
        
        prompt_enhancement = ad_type_prompts.get(ad_type, "Create compelling advertising copy.")
        
        if promotion:
            prompt_enhancement += f" Promotion details: {promotion}"
        
        enhanced_context = business_context.copy()
        enhanced_context['ad_type'] = prompt_enhancement
        
        result = self.gemini.generate_marketing_content(enhanced_context, content_type, 'ads')
        
        if result['success']:
            structured_ad = self._structure_ad_copy(result['content'], ad_type, promotion)
            result['structured_ad'] = structured_ad
        
        return result
    
    def generate_video_script(self, business_context: Dict, video_type: str, duration: str = "short") -> Dict:
        """Generate video scripts for social media"""
        content_type = "video_script"
        
        video_prompts = {
            'tutorial': "Create a step-by-step tutorial video script that educates viewers.",
            'testimonial': "Create a customer testimonial video script that builds trust.",
            'behind_scenes': "Create a behind-the-scenes video script that shows business authenticity.",
            'promotional': "Create a promotional video script that highlights offers and benefits.",
            'storytelling': "Create a storytelling video script that connects emotionally with viewers."
        }
        
        prompt_enhancement = video_prompts.get(video_type, "Create an engaging video script.")
        prompt_enhancement += f" Duration: {duration}"
        
        enhanced_context = business_context.copy()
        enhanced_context['video_type'] = prompt_enhancement
        
        result = self.gemini.generate_marketing_content(enhanced_context, content_type, 'video')
        
        if result['success']:
            structured_script = self._structure_video_script(result['content'], video_type, duration)
            result['structured_script'] = structured_script
        
        return result
    
    def generate_whatsapp_campaign(self, business_context: Dict, campaign_type: str) -> Dict:
        """Generate WhatsApp message campaigns"""
        content_type = "whatsapp"
        
        campaign_prompts = {
            'broadcast': "Create a WhatsApp broadcast message for customer announcements.",
            'sales': "Create a direct sales message for WhatsApp conversations.",
            'followup': "Create a follow-up message for recent customers.",
            'promotional': "Create a promotional message for special offers.",
            'engagement': "Create a message to re-engage inactive customers."
        }
        
        prompt_enhancement = campaign_prompts.get(campaign_type, "Create a professional WhatsApp message.")
        
        enhanced_context = business_context.copy()
        enhanced_context['campaign_type'] = prompt_enhancement
        
        result = self.gemini.generate_marketing_content(enhanced_context, content_type, 'whatsapp')
        
        if result['success']:
            structured_message = self._structure_whatsapp_message(result['content'], campaign_type)
            result['structured_message'] = structured_message
        
        return result
    
    def generate_email_campaign(self, business_context: Dict, email_type: str) -> Dict:
        """Generate email marketing content"""
        content_type = "email"
        
        email_prompts = {
            'newsletter': "Create a newsletter email that provides value and updates.",
            'promotional': "Create a promotional email with compelling offers.",
            'welcome': "Create a welcome email for new customers.",
            'abandoned_cart': "Create an abandoned cart recovery email.",
            're_engagement': "Create a re-engagement email for inactive subscribers."
        }
        
        prompt_enhancement = email_prompts.get(email_type, "Create a professional email.")
        
        enhanced_context = business_context.copy()
        enhanced_context['email_type'] = prompt_enhancement
        
        result = self.gemini.generate_marketing_content(enhanced_context, content_type, 'email')
        
        if result['success']:
            structured_email = self._structure_email_content(result['content'], email_type)
            result['structured_email'] = structured_email
        
        return result
    
    def _enhance_social_content(self, content: str, platform: str, theme: str) -> Dict:
        """Enhance social media content with structured data"""
        # Extract hashtags
        hashtags = self._extract_hashtags(content)
        
        # Generate platform-specific recommendations
        posting_tips = self._get_posting_tips(platform)
        
        # Estimate engagement metrics
        engagement_metrics = self._estimate_engagement(platform, len(content))
        
        return {
            'content': content,
            'hashtags': hashtags,
            'character_count': len(content),
            'platform': platform,
            'posting_tips': posting_tips,
            'estimated_engagement': engagement_metrics,
            'theme': theme,
            'optimal_post_times': self._get_optimal_times(platform)
        }
    
    def _structure_product_description(self, content: str, product_details: Dict) -> Dict:
        """Structure product description with key elements"""
        return {
            'description': content,
            'key_features': self._extract_key_points(content),
            'target_audience': product_details.get('target_customer', ''),
            'seo_keywords': self._extract_keywords(content),
            'call_to_action': self._generate_cta('product')
        }
    
    def _structure_ad_copy(self, content: str, ad_type: str, promotion: Dict = None) -> Dict:
        """Structure ad copy with campaign elements"""
        return {
            'headline': self._extract_headline(content),
            'body': content,
            'call_to_action': self._generate_cta(ad_type),
            'ad_type': ad_type,
            'promotion_details': promotion,
            'targeting_suggestions': self._get_ad_targeting(ad_type)
        }
    
    def _structure_video_script(self, content: str, video_type: str, duration: str) -> Dict:
        """Structure video script with timing and elements"""
        return {
            'script': content,
            'video_type': video_type,
            'estimated_duration': duration,
            'key_scenes': self._extract_scenes(content),
            'call_to_action': self._generate_cta('video'),
            'platform_optimization': self._get_video_platform_tips(video_type)
        }
    
    def _structure_whatsapp_message(self, content: str, campaign_type: str) -> Dict:
        """Structure WhatsApp message with engagement elements"""
        return {
            'message': content,
            'campaign_type': campaign_type,
            'character_count': len(content),
            'suggested_replies': self._generate_suggested_replies(campaign_type),
            'timing_suggestions': self._get_whatsapp_timing(),
            'personalization_tips': self._get_whatsapp_personalization()
        }
    
    def _structure_email_content(self, content: str, email_type: str) -> Dict:
        """Structure email content with marketing elements"""
        return {
            'subject_line': self._generate_email_subject(content, email_type),
            'body': content,
            'email_type': email_type,
            'key_sections': self._extract_email_sections(content),
            'call_to_action': self._generate_cta('email'),
            'personalization_fields': ['{name}', '{business}', '{location}']
        }
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract or generate relevant hashtags"""
        hashtags = re.findall(r'#\w+', content)
        if not hashtags:
            # Generate some generic business hashtags
            hashtags = ['#smallbusiness', '#localbusiness', '#supportlocal', '#entrepreneur']
        return hashtags[:10]  # Limit to 10 hashtags
    
    def _get_posting_tips(self, platform: str) -> List[str]:
        """Get platform-specific posting tips"""
        tips = {
            'facebook': [
                "Post during business hours (9 AM - 5 PM)",
                "Use high-quality images or videos",
                "Ask questions to encourage comments",
                "Use Facebook Insights to track performance"
            ],
            'instagram': [
                "Post during lunch (11 AM - 1 PM) or evening (7 PM - 9 PM)",
                "Use relevant hashtags (5-10 per post)",
                "Engage with comments quickly",
                "Use Instagram Stories for daily updates"
            ],
            'tiktok': [
                "Post during evening hours (7 PM - 11 PM)",
                "Use trending sounds and effects",
                "Keep videos short and engaging (15-30 seconds)",
                "Participate in trending challenges"
            ],
            'whatsapp': [
                "Send messages during business hours",
                "Keep messages personal and concise",
                "Include clear call-to-action",
                "Don't spam - respect customer privacy"
            ]
        }
        return tips.get(platform.lower(), ["Post consistently", "Engage with your audience"])
    
    def _estimate_engagement(self, platform: str, content_length: int) -> Dict:
        """Estimate potential engagement metrics"""
        base_metrics = {
            'facebook': {'likes': 50, 'comments': 5, 'shares': 2},
            'instagram': {'likes': 100, 'comments': 10, 'saves': 5},
            'tiktok': {'likes': 200, 'comments': 15, 'shares': 10},
            'twitter': {'likes': 30, 'retweets': 5, 'replies': 3},
            'whatsapp': {'reads': 80, 'replies': 20}
        }
        
        return base_metrics.get(platform.lower(), {'likes': 50, 'engagement': 'medium'})
    
    def _get_optimal_times(self, platform: str) -> List[str]:
        """Get optimal posting times for platform"""
        times = {
            'facebook': ["9:00 AM", "1:00 PM", "7:00 PM"],
            'instagram': ["11:00 AM", "2:00 PM", "8:00 PM"],
            'tiktok': ["7:00 PM", "9:00 PM", "11:00 PM"],
            'twitter': ["8:00 AM", "12:00 PM", "6:00 PM"],
            'whatsapp': ["10:00 AM", "4:00 PM", "7:00 PM"]
        }
        return times.get(platform.lower(), ["Morning", "Afternoon", "Evening"])
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content"""
        sentences = content.split('. ')
        return [s.strip() for s in sentences if len(s.strip()) > 10][:5]
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract potential SEO keywords"""
        words = content.lower().split()
        # Simple keyword extraction - in production, use proper NLP
        keywords = [word for word in words if len(word) > 5]
        return list(set(keywords))[:10]
    
    def _generate_cta(self, content_type: str) -> str:
        """Generate call-to-action based on content type"""
        ctas = {
            'product': "Shop now!",
            'sales': "Limited time offer!",
            'video': "Watch now!",
            'email': "Click here to learn more!",
            'social_post': "Like and share!",
            'whatsapp': "Reply to get started!"
        }
        return ctas.get(content_type, "Learn more!")
    
    def _extract_headline(self, content: str) -> str:
        """Extract or generate headline from content"""
        first_line = content.split('\n')[0]
        return first_line[:100]  # Limit headline length
    
    def _extract_scenes(self, content: str) -> List[str]:
        """Extract scenes from video script"""
        scenes = content.split('\n\n')
        return [scene.strip() for scene in scenes if scene.strip()][:5]
    
    def _generate_suggested_replies(self, campaign_type: str) -> List[str]:
        """Generate suggested replies for WhatsApp"""
        replies = {
            'sales': ["Yes, I'm interested!", "Tell me more", "Send me the details"],
            'followup': ["Great, thanks!", "I'll be there", "See you soon"],
            'promotional': ["Awesome deal!", "I want this!", "How do I get it?"]
        }
        return replies.get(campaign_type, ["Thanks!", "Got it", "Interesting"])
    
    def _get_whatsapp_timing(self) -> List[str]:
        """Get optimal WhatsApp messaging times"""
        return ["Weekdays 10 AM - 12 PM", "Weekdays 4 PM - 6 PM", "Avoid late nights"]
    
    def _get_whatsapp_personalization(self) -> List[str]:
        """Get WhatsApp personalization tips"""
        return ["Use customer name", "Reference past purchases", "Keep it conversational"]
    
    def _generate_email_subject(self, content: str, email_type: str) -> str:
        """Generate email subject line"""
        first_sentence = content.split('.')[0]
        subjects = {
            'newsletter': f"Update: {first_sentence[:50]}",
            'promotional': f"Special Offer: {first_sentence[:40]}",
            'welcome': "Welcome to Our Business!",
            'abandoned_cart': "Did you forget something?",
            're_engagement': "We miss you!"
        }
        return subjects.get(email_type, first_sentence[:60])
    
    def _extract_email_sections(self, content: str) -> List[str]:
        """Extract email sections"""
        paragraphs = content.split('\n\n')
        return [p.strip() for p in paragraphs if len(p.strip()) > 20][:4]
    
    def _get_ad_targeting(self, ad_type: str) -> List[str]:
        """Get ad targeting suggestions"""
        targeting = {
            'sales': ["Local customers", "Past buyers", "Similar interests"],
            'awareness': ["Broad audience", "Local area", "Interest-based"],
            'promotional': ["Price-sensitive", "Bargain hunters", "Local deals"]
        }
        return targeting.get(ad_type, ["Local audience", "Interest-based"])
    
    def _get_video_platform_tips(self, video_type: str) -> List[str]:
        """Get video platform optimization tips"""
        tips = {
            'tutorial': ["Add text overlays", "Use clear steps", "Show results"],
            'testimonial': ["Show real customers", "Authentic stories", "Before/after"],
            'promotional': ["Highlight benefits", "Create urgency", "Clear CTA"]
        }
        return tips.get(video_type, ["Engaging thumbnail", "Clear audio", "Good lighting"])