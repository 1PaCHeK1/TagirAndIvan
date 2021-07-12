from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test(request):
    print(request)
    return Response({'username' : "vasua"}, status=200)
