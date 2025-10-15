from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'name', 'age', 
            'average_cycle', 'selected_mode', 'menstrual_mode'
        )
        read_only_fields = ('email', 'menstrual_mode')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get user profile
        serializer = UserProfileSerializer(self.user.profile)
        
        # Add profile data to the response
        data['user'] = serializer.data
        
        # Rename 'access' to 'access_token' to match frontend
        data['access_token'] = data.pop('access')
        
        # Remove refresh token from response, as frontend doesn't need it on login
        data.pop('refresh', None)
        
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, min_length=8)
    # --- FIX STARTS HERE ---
    # Mark fields that are not on the User model as write_only
    name = serializers.CharField(required=True, write_only=True)
    age = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    average_cycle = serializers.IntegerField(required=False, default=28, write_only=True)
    # The 'mode' field is not used in the create method, but making it write_only is correct practice
    mode = serializers.CharField(required=False, default='Menstrual', write_only=True)
    # --- FIX ENDS HERE ---

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'age', 'average_cycle', 'mode')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create UserProfile with extra data
        UserProfile.objects.create(
            user=user,
            name=validated_data['name'],
            age=validated_data.get('age'),
            average_cycle=validated_data.get('average_cycle', 28),
        )
        return user