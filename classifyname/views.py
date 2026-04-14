from django.shortcuts import render
# import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from email.utils import parsedate_to_datetime
from datetime import timezone
from django.core.cache import cache
import httpx

http_client = httpx.Client(timeout=10.0, limits=httpx.Limits(max_connections=10, max_keepalive_connections=5))


class Query(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"status": "error", "message": 'Name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if name.isdigit():
            return Response({"status": "error", "message": 'Name parameter must be a string.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        cache_name = f'classifyname:{name.lower()}'
        cached_result = cache.get(cache_name)
        if cached_result:
            return Response(
                {"status": "success",
                "data": cached_result},
                status=status.HTTP_200_OK
            )

        # Call the external API to classify the name
        try:
            api_url = f'https://api.genderize.io?name={name}'
            response = httpx.get(api_url, params={'name': name})

            if response.status_code == 200:
                data = response.json()

                if data.get('gender') == None or data.get('count', 0) == 0:
                    return Response({"status": "error", "message": 'No prediction available for the provided name.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                probability = data.get('probability', 0)
                sample_size = data.get('count', 0)

                if probability >= 0.7 and sample_size >= 100:
                    is_confident = True
                else:
                    is_confident = False

                processed_time_string = response.headers.get('Date')
                processed_time = parsedate_to_datetime(processed_time_string).astimezone(timezone.utc).isoformat() if processed_time_string else None
                result = {
                    'name': data.get('name'),
                    'gender': data.get('gender'),
                    'probability': probability,
                    'sample_size': sample_size,
                    'is_confident': is_confident,
                    'processed_at': processed_time,
                }
                cache.set(cache_name, result)

                return Response({"status": "success", "data": result}, status=status.HTTP_200_OK)
                
            else:
                return Response({"status": "error", "message": 'Failed to classify the name.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)