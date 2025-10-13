from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PostpartumMoodLog
from .serializers import PostpartumMoodLogSerializer

class PostpartumMoodLogView(views.APIView):
    """
    GET, POST, or UPDATE a postpartum mood log for a specific date.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, date_str):
        try:
            log_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            log = PostpartumMoodLog.objects.get(user=request.user, date=log_date)
            serializer = PostpartumMoodLogSerializer(log)
            return Response(serializer.data)
        except PostpartumMoodLog.DoesNotExist:
            return Response({"detail": "No log found for this date."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, date_str):
        try:
            log_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            # Add the date to the request data for validation
            request.data['date'] = log_date
            
            # Use get_or_create to handle both creation and updates
            log, created = PostpartumMoodLog.objects.get_or_create(
                user=request.user, 
                date=log_date,
                defaults={'mood': request.data.get('mood')}
            )

            # If the object was not created, it means it already existed, so we update it
            if not created:
                serializer = PostpartumMoodLogSerializer(log, data=request.data)
            else:
                serializer = PostpartumMoodLogSerializer(log, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
                return Response(serializer.data, status=response_status)
            
            # If invalid, and we created a placeholder, delete it.
            if created:
                log.delete()
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)