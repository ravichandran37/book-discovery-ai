from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_smart_recommendation

class DiscoveryAPIView(APIView):
    def post(self, request):
        user_query = request.data.get('query', '')
        
        if not user_query:
            return Response(
                {"error": "Please provide a 'query' in the request body."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Call our AI service
            result = get_smart_recommendation(user_query)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from django.shortcuts import render
def home_page(request):
    return render(request, 'index.html')


class DiscoveryAPIView(APIView):
    def post(self, request):
        user_query = request.data.get('query', '')
        history = request.data.get('history', []) # Get history from frontend
        
        if not user_query:
            return Response({"error": "No query"}, status=400)
            
        result = get_smart_recommendation(user_query, history)
        return Response(result)