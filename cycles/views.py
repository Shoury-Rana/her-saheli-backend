from datetime import timedelta
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from .models import Cycle, DailyLog
from .serializers import CycleSerializer, DailyLogSerializer

class CycleLogView(views.APIView):
    """
    Handles listing cycles (GET) and logging period start/end (POST).
    """
    def get(self, request):
        """List all cycles for the authenticated user."""
        cycles = Cycle.objects.filter(user=request.user)
        serializer = CycleSerializer(cycles, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new cycle (log period start) or update the last cycle (log period end).
        - To log start: POST { "start_date": "YYYY-MM-DD" }
        - To log end: POST { "end_date": "YYYY-MM-DD" } (even if start_date is also sent)
        """
        data = request.data
        user = request.user

        # Case 1: End Period. Identified by the presence of 'end_date'.
        if 'end_date' in data:
            last_cycle = Cycle.objects.filter(user=user, end_date__isnull=True).order_by('-start_date').first()
            
            if last_cycle:
                serializer = CycleSerializer(last_cycle, data=data, partial=True)
                if serializer.is_valid():
                    # Additional validation to prevent end_date from being before start_date
                    if serializer.validated_data.get('end_date') < last_cycle.start_date:
                        return Response({"end_date": ["End date cannot be before the start date."]}, status=status.HTTP_400_BAD_REQUEST)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "No active period found to end."}, status=status.HTTP_400_BAD_REQUEST)

        # Case 2: Start Period. Identified by presence of 'start_date' and absence of 'end_date'.
        elif 'start_date' in data:
            if Cycle.objects.filter(user=user, end_date__isnull=True).exists():
                    return Response({"error": "An active period already exists. End it before starting a new one."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CycleSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Case 3: Invalid data
        return Response({"error": "Provide 'start_date' to begin a period or 'end_date' to end the current one."}, status=status.HTTP_400_BAD_REQUEST)

class DailyLogView(views.APIView):
    def get(self, request, date_str):
        try:
            log_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            log = DailyLog.objects.get(user=request.user, date=log_date)
            serializer = DailyLogSerializer(log)
            return Response(serializer.data)
        except DailyLog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, date_str):
        try:
            log_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            log, created = DailyLog.objects.get_or_create(user=request.user, date=log_date)
            serializer = DailyLogSerializer(log, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)


class UnifiedPredictionView(views.APIView):
    """
    Provides cycle predictions including next period, ovulation, and fertile window.
    """
    def get(self, request):
        cycles = Cycle.objects.filter(user=request.user).order_by('-start_date')[:6]
        
        if cycles.count() < 2:
            return Response({"message": "Not enough cycle data to make a prediction."}, status=status.HTTP_404_NOT_FOUND)

        cycle_lengths = []
        for i in range(len(cycles) - 1):
            if cycles[i].start_date and cycles[i+1].start_date:
                length = (cycles[i].start_date - cycles[i+1].start_date).days
                if 15 < length < 45: # Filter out abnormal cycle lengths
                    cycle_lengths.append(length)

        if not cycle_lengths:
            avg_cycle_length = request.user.profile.average_cycle if hasattr(request.user, 'profile') else 28
        else:
            avg_cycle_length = sum(cycle_lengths) // len(cycle_lengths)

        last_cycle_start = cycles[0].start_date
        predicted_next_start = last_cycle_start + timedelta(days=avg_cycle_length)
        
        # Ovulation is typically 14 days before the next period
        estimated_ovulation = predicted_next_start - timedelta(days=14)
        
        # Fertile window is about 5 days before ovulation and the day of ovulation
        fertile_window_start = estimated_ovulation - timedelta(days=5)
        fertile_window_end = estimated_ovulation

        # Match the keys expected by the frontend: `next_period`, `ovulation_day`
        return Response({
            "next_period": predicted_next_start,
            "average_cycle_length": avg_cycle_length,
            "fertile_window_start": fertile_window_start,
            "fertile_window_end": fertile_window_end,
            "ovulation_day": estimated_ovulation,
        })