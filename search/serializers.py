from rest_framework import serializers
from .models import SearchResults

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    search = serializers.CharField()
    page = serializers.IntegerField()
    class Meta:
        model = SearchResults
        fields = ('page','search')