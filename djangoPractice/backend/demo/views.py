from django.shortcuts import render
# from django.http import Response, Response
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Demo
from .serializers import DemoSerializers
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import UserSerializers
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets

"""
Refactoring to use ViewSets
"""
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers

class DemoViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Demo.objects.all()
    serializer_class = DemoSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


"""
Creating an endpoint for the root of our API
"""

@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('users-list',request=request),
        'demo':  reverse('demo-list', request=request)

})

"""
Creating an endpoint for the highlighted snippets
"""

class DemoHighlighted(generics.GenericAPIView):
    queryset = Demo.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        demo = self.get_object()
        print(demo)
        return Response(demo.title)



"""
User generic class based views
"""
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers





"""
Using generic class-based views
"""
class DemoListGenerics(generics.ListCreateAPIView):
    queryset=Demo.objects.all()
    serializer_class = DemoSerializers

class DemoDetailsGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

"""
Below is Mixin based view
"""
class DemoListMixin(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DemoDetailsMixin(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin
                       ,generics.GenericAPIView):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializers
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        # pk = kwargs.get("pk")
        # if pk is not None:
        #     return self.retrieve(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    





"""
Below is Class based view
"""

class DemoViewList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request):
        demo = Demo.objects.all()
        serializers = DemoSerializers(demo, many=True)
        return Response(serializers.data)

    
    def post(self, request):
        serializers = DemoSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    # def put(self, request):
    #     demo = Demo.objects.all()
    #     serializers = DemoSerializers(demo,data=request.data)
    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response(serializers.data)
    # def delete(self, request):
    #     demo = Demo.objects.all()
    #     demo.delete()
    #     return Response(status=204, content_type="application/json")

class DemoViewDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Demo.objects.get(pk=pk)
        except Demo.DoesNotExist:
            return Http404
        
    def get(self, request, pk):
        demo = self.get_object(pk)
        serializer = DemoSerializers(demo)
        return Response(serializer.data)
    
    def put(self, request, pk):
        demo = self.get_object(pk)
        serializer = DemoSerializers(demo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        demo = self.get_object(pk)
        demo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






"""
Below is Function based view
"""

# @csrf_exempt
@api_view(['GET', 'POST'])
def demo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        demo = Demo.objects.all()
        print({demo})
        print(Demo.objects.all())
        serializers = DemoSerializers(demo, many=True)
        print(serializers.data)
        return Response(serializers.data, safe=False)
    
    elif request.method == 'POST':
        print("hello world")
        # data = JSONParser().parse(request)
        serializers = DemoSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)
        return Response(serializers.errors, status=400)
    

@api_view(['GET', 'PUT', 'DELETE'])
def demo_details(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        demo = Demo.objects.get(pk=pk)
    except Demo.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializers = DemoSerializers(demo)
        return Response(serializers.data)
    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializers = DemoSerializers(demo,data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=400)
    elif request.method == 'DELETE':
        demo.delete()
        return Response(status=204, content_type="application/json")



