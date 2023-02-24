from rest_framework import serializers
from .models import SearchResults

class SearchCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResults
        fields = '__all__'
