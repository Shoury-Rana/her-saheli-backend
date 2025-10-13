from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PregnancyProfile
from .serializers import PregnancyProfileSerializer

class PregnancyProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the pregnancy profile for the authenticated user.
    If a profile doesn't exist, one will be created upon first access.
    """
    serializer_class = PregnancyProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # Retrieve or create a pregnancy profile for the logged-in user
        profile, created = PregnancyProfile.objects.get_or_create(user=self.request.user)
        return profile