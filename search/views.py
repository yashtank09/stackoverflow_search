from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests

API_URL = "https://api.stackexchange.com/2.3/search/advanced"

# Create your views here.
@csrf_exempt
def get_questions(req, page=1):
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
    return render(req, 'search/search_questions.html', {'requested_data': 'No data found!'})