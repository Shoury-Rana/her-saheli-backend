from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Cycle, DailyLog
from .serializers import CycleSerializer, DailyLogSerializer

class CycleViewSet(viewsets.ModelViewSet):
    serializer_class = CycleSerializer

    def get_queryset(self):
        return Cycle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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


class MenstrualPredictionView(views.APIView):
    def get(self, request):
        cycles = Cycle.objects.filter(user=request.user).order_by('-start_date')[:6]
        
        if cycles.count() < 2:
            return Response({"message": "Not enough cycle data to make a prediction."}, status=status.HTTP_404_NOT_FOUND)

        cycle_lengths = []
        for i in range(len(cycles) - 1):
            length = (cycles[i].start_date - cycles[i+1].start_date).days
            if 15 < length < 45: # Filter out abnormal cycle lengths for better prediction
                cycle_lengths.append(length)

        if not cycle_lengths:
            avg_cycle_length = 28 # Default if no valid cycles
        else:
            avg_cycle_length = sum(cycle_lengths) // len(cycle_lengths)

        last_cycle_start = cycles[0].start_date
        predicted_next_start = last_cycle_start + timedelta(days=avg_cycle_length)
        
        return Response({
            "predicted_next_cycle_start": predicted_next_start,
            "average_cycle_length": avg_cycle_length
        })

class TTCPredictionView(views.APIView):
    def get(self, request):
        # This view reuses the logic from MenstrualPredictionView
        prediction_view = MenstrualPredictionView()
        prediction_response = prediction_view.get(request)

        if prediction_response.status_code != 200:
            return prediction_response # Pass on the "not enough data" message

        predicted_start_str = prediction_response.data.get("predicted_next_cycle_start")
        predicted_start = timezone.datetime.strptime(predicted_start_str, '%Y-%m-%d').date()
        
        # Ovulation is typically 14 days before the next period
        estimated_ovulation = predicted_start - timedelta(days=14)
        
        # Fertile window is about 5 days before ovulation and the day of ovulation
        fertile_window_start = estimated_ovulation - timedelta(days=5)
        fertile_window_end = estimated_ovulation

        return Response({
            "fertile_window_start": fertile_window_start,
            "fertile_window_end": fertile_window_end,
            "estimated_ovulation_date": estimated_ovulation
        })