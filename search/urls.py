from django.urls import path
from .views import StackoverflowAPI, getQuestions
from .views import SearchAPIView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', StackoverflowAPI.search),
    path('questions/', getQuestions, name='questions'),
    path('search/', SearchAPIView.as_view(), name='search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)