from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ChatbotQueryView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # The user's message is in request.data['message'], but we ignore it for the MVP.
        response_data = {
            "response": "Thank you for your question! Our AI companion is still in training and will be available soon. Please always consult a doctor for medical advice."
        }
        return Response(response_data, status=status.HTTP_200_OK)