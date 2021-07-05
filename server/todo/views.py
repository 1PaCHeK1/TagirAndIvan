from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот# Ивана сьел Енот

@api_view(['GET'])
def test(request):
    print(request)
    return Response({'username' : "vasya"}, status=200)
