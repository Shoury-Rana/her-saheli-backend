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
        """
        List all individual period dates for the authenticated user in a flat list.
        e.g., ["2025-10-01", "2025-10-02", ...]
        """
        cycles = Cycle.objects.filter(user=request.user)
        all_period_dates = []
        
        for cycle in cycles:
            start_date = cycle.start_date
            # If end_date is None, it's an ongoing period. Use today's date as the end for display purposes.
            end_date = cycle.end_date if cycle.end_date else timezone.now().date()
            
            # Ensure start_date is not after end_date for the loop
            if start_date > end_date:
                continue

            current_date = start_date
            while current_date <= end_date:
                all_period_dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)
                
        return Response(all_period_dates)

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
    Provides cycle predictions as a list of events, each with a date and type.
    Types can be 'next_period', 'ovulation_day', or 'fertile_window'.
    e.g., [{'date': '...', 'type': 'next_period'}, ...]
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

        # Create a list of prediction objects as required by the frontend
        predictions_list = []

        # Add next period date
        predictions_list.append({
            "date": predicted_next_start.strftime('%Y-%m-%d'),
            "type": "next_period"
        })

        # Add ovulation day
        predictions_list.append({
            "date": estimated_ovulation.strftime('%Y-%m-%d'),
            "type": "ovulation_day"
        })

        # Add all dates in the fertile window
        current_date = fertile_window_start
        while current_date <= fertile_window_end:
            predictions_list.append({
                "date": current_date.strftime('%Y-%m-%d'),
                "type": "fertile_window"
            })
            current_date += timedelta(days=1)

        return Response(predictions_list)


class DayLogToggleView(views.APIView):
    """
    Handles adding or removing a single period day.
    POST to add a day.
    DELETE to remove a day.
    """
    def _parse_date(self, date_str):
        try:
            return timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None

    def post(self, request, date_str):
        """
        Add a period log for a specific day.
        This can result in creating a new cycle, extending an existing one,
        or merging two adjacent cycles.
        """
        date = self._parse_date(date_str)
        if not date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # 1. Check if the date is already part of an existing cycle.
        if Cycle.objects.filter(user=user, start_date__lte=date, end_date__gte=date).exists():
            return Response(status=status.HTTP_200_OK) # Date already logged, do nothing.

        # 2. Check for adjacent cycles.
        prev_cycle = Cycle.objects.filter(user=user, end_date=date - timedelta(days=1)).first()
        next_cycle = Cycle.objects.filter(user=user, start_date=date + timedelta(days=1)).first()

        # 3a. Both previous and next cycles exist -> Merge them.
        if prev_cycle and next_cycle:
            prev_cycle.end_date = next_cycle.end_date
            prev_cycle.save()
            next_cycle.delete()
            return Response(status=status.HTTP_200_OK)
        
        # 3b. Only a previous cycle exists -> Extend it.
        if prev_cycle:
            prev_cycle.end_date = date
            prev_cycle.save()
            return Response(status=status.HTTP_200_OK)

        # 3c. Only a next cycle exists -> Extend it.
        if next_cycle:
            next_cycle.start_date = date
            next_cycle.save()
            return Response(status=status.HTTP_200_OK)
            
        # 4. No adjacent cycles -> Create a new single-day cycle.
        Cycle.objects.create(user=user, start_date=date, end_date=date)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, date_str):
        """
        Remove a period log for a specific day.
        This can result in deleting a cycle, shortening it, or splitting it into two.
        """
        date = self._parse_date(date_str)
        if not date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        
        # 1. Find the cycle containing the date.
        cycle = Cycle.objects.filter(user=user, start_date__lte=date, end_date__gte=date).first()

        if not cycle:
            return Response(status=status.HTTP_204_NO_CONTENT) # No cycle to delete from.

        # 2a. Case: Single-day cycle.
        if cycle.start_date == cycle.end_date:
            cycle.delete()
        
        # 2b. Case: Date is the start date.
        elif cycle.start_date == date:
            cycle.start_date += timedelta(days=1)
            cycle.save()

        # 2c. Case: Date is the end date.
        elif cycle.end_date == date:
            cycle.end_date -= timedelta(days=1)
            cycle.save()
            
        # 2d. Case: Date is in the middle -> Split the cycle.
        else:
            original_end_date = cycle.end_date
            # Update the existing cycle to end before the deleted date.
            cycle.end_date = date - timedelta(days=1)
            cycle.save()
            
            # Create a new cycle for the part after the deleted date.
            Cycle.objects.create(
                user=user,
                start_date=date + timedelta(days=1),
                end_date=original_end_date
            )
            
        return Response(status=status.HTTP_204_NO_CONTENT)