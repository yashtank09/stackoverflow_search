from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
import requests

API_URL = "https://api.stackexchange.com/2.3/search/advanced"


# Create your views here.

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


@api_view(['GET'])
def getQuestions(req, page=1):
    query = req.GET['query']
    parameters = {
        'page': page,
        'order': 'asc',
        'q':  query, # 'TypeError: SerializerMetaclass object is not iterable',
        'sort':'activity',
        'answers': 3,
        'site': 'stackoverflow'
    }
    response = requests.get(API_URL, params=parameters)
    requested_data = response.json()

    return Response(requested_data)