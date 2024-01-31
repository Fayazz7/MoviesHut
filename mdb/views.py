from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.decorators import action

# Create your views here.
from mdb.serializers import UserSerializer,MovieSerializer,UserProfileSerializer,ReviewSerializer
from mdb.models import Genre,Movie,UserProfile
# Create your views here.

class RegistrationView(APIView):
    def post (self,request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class MovieView(ModelViewSet):
    
    serializer_class=MovieSerializer
    queryset=Movie.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    @action(methods=["post"], detail=True)
    def addreview(self, request, *args, **kwargs):
        id = int(kwargs.get("pk"))
        m_obj = Movie.objects.get(id=id)
        # print(m_obj)
        r_obj=request.user.r_user.all().values_list("movie",flat=True)
        print(r_obj)
        print(type(id))
        if id in r_obj:
            raise serializers.ValidationError("Already Reviewd")
        else:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user, movie=m_obj)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    
    @action(methods=["post","delete"],detail=True)
    def addtowatch(self,request,*args, **kwargs):
        id=int(kwargs.get("pk"))
        m_obj=Movie.objects.get(id=id)
        w_obj=request.user.profile.watchlist.all()
        print(w_obj)
        if request.method == "POST":
            request.user.profile.watchlist.add(m_obj)
            return Response (data="Movie Added")
        elif request.method == "DELETE":
            request.user.profile.watchlist.remove(m_obj)
            return Response (data="Movie Removed")
    
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    
    
class UserProfileView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def update(self,request,*args, **kwargs):
        user_obj=request.user.profile
        user_obj_id=request.user.profile.user_id
        if user_obj_id == int(kwargs.get("pk")):
            serializer=UserProfileSerializer(data=request.data,instance=user_obj)
            if serializer.is_valid():
                serializer.save()
                return Response (data=serializer.data)
            else:
                return Response (data=serializer.errors)
        else:
            raise serializers.ValidationError ("Permission Denied")
        
    def retrieve(self,request,*args, **kwargs):
        user_obj=request.user.profile
        print(user_obj)
        print(kwargs.get("pk"))
        print(request.user.id)
        if request.user.id == int(kwargs.get("pk")):
            serializer=UserProfileSerializer(user_obj)
            return Response (data=serializer.data)
        else:
            raise serializers.ValidationError("Permission Needed")
        
    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    