from django.urls import path
from .views import StackoverflowAPI, getQuestions

urlpatterns = [
    path('', StackoverflowAPI.search),
    path('questions/', getQuestions, name='questions'),
]