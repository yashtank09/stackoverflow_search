from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from .serializers import SearchCacheSerializer
import requests

API_URL = "https://api.stackexchange.com/2.3/search/advanced"


# starting with simple function based view and showing data on webpage(html)

class StackoverflowAPI:
    @csrf_exempt
    def search(req, page=1):
        if req.method == 'POST':
            parameters = {
                'page': page,
                'order': 'asc',
                'q': req.POST.get('query'),
                'answers': 3,
                'site': 'stackoverflow'
            }
            response = requests.get(API_URL, params=parameters)
            requested_data = response.json()

            if response:
                return render(req, 'search/search_questions.html', {'requested_data': requested_data['items']})
        return render(req, 'search/search_questions.html', {'requested_data': '200'})


# dummy restAPI function view
@api_view(['GET'])
def getQuestions(req, page=1):
    query = req.GET['query']
    parameters = {
        'page': page,
        'order': 'asc',
        'q': query,  # 'TypeError: SerializerMetaclass object is not iterable',
        'sort': 'activity',
        'answers': 3,
        'site': 'stackoverflow'
    }
    response = requests.get(API_URL, params=parameters)
    requested_data = response.json()

    return Response(requested_data)


# class based RestAPI view
class SearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', 'XYZ error')
        page = request.GET.get('page', 1)

        # Check if the query is already cached
        cache_key = f'search:{query}:{page}'
        cached_results = cache.get(cache_key)
        if cached_results is not None:
            serializer = SearchCacheSerializer(data=cached_results)
            serializer.is_valid()
            return Response(serializer.validated_data)

        # If not cached, fetch the results from the StackOverflow API
        # url = 'https://api.stackexchange.com/2.3/search/advanced'
        params = {
            'page': page,
            'order': 'asc',
            'q': query,
            'sort': 'activity',
            'answers': 3,
            'site': 'stackoverflow'
        }
        headers = {'User-Agent': 'stackoverflow-search-app'}
        response = requests.get(API_URL, params=params)

        # Cache the results
        if response.status_code == 200:
            data = {
                'query': query,
                'results': response.json(),
            }
            serializer = SearchCacheSerializer(data=data)
            serializer.is_valid()
            cache.set(cache_key, serializer.validated_data, 60 * 60)
            return Response(serializer.data)

        return Response({'error': 'An error occurred while fetching the results.'}, status=response.status_code)
