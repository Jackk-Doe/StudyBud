# Without Rest framework
from django.http import JsonResponse

# This view shows all routes in api
def getRoutes_NO_REST(reqeust):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    # By setting safe=False : to convert data(routes) to be JSON data
    return JsonResponse(routes, safe=False)



# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])  #Specified HTTP Method is allowed to access this view 
def getRoutes(reqeust):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()

    # Set [many] to True when serializing many objects
    serializer = RoomSerializer(rooms, many=True)

    # See the differences
    # print(serializer, "\n")
    # print(serializer.data)

    # return serialized obj format by specified .data
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data)