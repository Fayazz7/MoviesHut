from rest_framework import serializers
from django.contrib.auth.models import User

from mdb.models import Movie,Genre,UserProfile,Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields="__all__"
        read_only_fields=["id","created_at","updated_at","is_active"]

class ReviewSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()
    movie=serializers.StringRelatedField()
    class Meta:
        model=Review
        fields="__all__"
        read_only_fields=["id","owner","movie","created_at","updated_at","is_active"]

class MovieSerializer(serializers.ModelSerializer):
    reviewcount=serializers.IntegerField()
    reviews=ReviewSerializer(read_only=True,many=True)
    genre=serializers.StringRelatedField(many=True)
    # genre=GenreSerializer(many=True,read_only=True)
    language=serializers.StringRelatedField()
    class Meta:
        model=Movie
        fields="__all__"
        
class UserProfileSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(read_only=True,many=True)
    watchlist= MovieSerializer(read_only=True,many=True)
    user=serializers.StringRelatedField()
    class Meta:
        model=UserProfile
        fields="__all__"
        read_only_fields=["id","user","watchlist","created_at","updated_at","is_active"]
        
