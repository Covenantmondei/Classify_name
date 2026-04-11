from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from email.utils import parsedate_to_datetime
from datetime import timezone
from django.core.cache import cache

class Query(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'error': 'Name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if name.isdigit():
            return Response({'error': 'Name parameter must be a string.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        cache_name = f'classifyname:{name.lower()}'
        cached_result = cache.get(cache_name)
        if cached_result:
            return Response(
                cached_result,
                status=status.HTTP_200_OK
            )

        # Call the external API to classify the name
        try:
            api_url = f'https://api.genderize.io?name={name}'
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()

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

                return Response(result, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Failed to classify the name.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)