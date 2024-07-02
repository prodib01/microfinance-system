from rest_framework import serializers
from clientApp.models import Person

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'