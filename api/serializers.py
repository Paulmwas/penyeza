from rest_framework import serializers
from .models import BusinessProfile, GrowthPlan, MarketingContent
from users.models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'phone_number')
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        read_only_fields = ('user', 'id', 'created_at', 'updated_at')

class GrowthPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthPlan
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class MarketingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingContent
        fields = '__all__'
        read_only_fields = ('id', 'business', 'created_at')

class ContentGenerationRequestSerializer(serializers.Serializer):
    content_type = serializers.ChoiceField(choices=[
        'social_post', 'product_desc', 'ad_copy', 'video_script', 'email', 'whatsapp'
    ])
    platform = serializers.CharField(required=False)
    theme = serializers.CharField(required=False, allow_blank=True)
    tone = serializers.CharField(required=False, default='professional')