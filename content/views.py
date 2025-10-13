from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import StaticContent
from .serializers import StaticContentSerializer

class StaticContentView(generics.ListAPIView):
    """
    List static content like tips, guides, and FAQs.
    Filterable by query parameters:
    - `mode`: e.g., 'MENSTRUAL', 'TTC', 'PREGNANCY'
    - `type`: e.g., 'TIP', 'FAQ', 'GUIDE'
    - `week`: e.g., 8, 20 (for pregnancy guides)
    """
    serializer_class = StaticContentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = StaticContent.objects.all()
        
        # Filter by relevant health mode
        mode = self.request.query_params.get('mode')
        if mode:
            queryset = queryset.filter(relevant_mode__iexact=mode)
            
        # Filter by content type
        content_type = self.request.query_params.get('type')
        if content_type:
            queryset = queryset.filter(content_type__iexact=content_type)

        # Filter by week of pregnancy (only for pregnancy guides)
        week = self.request.query_params.get('week')
        if week and week.isdigit():
            queryset = queryset.filter(week_of_pregnancy=int(week))
            
        return queryset