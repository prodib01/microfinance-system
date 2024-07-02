from rest_framework.response import Response
from rest_framework.views import APIView
from clientApp.models import Person
from .serializers import ClientSerializer

class ClientViewSet(APIView):
    def get(self, request):
        clients = Person.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)