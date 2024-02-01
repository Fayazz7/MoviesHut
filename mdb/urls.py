from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from mdb import views

router = DefaultRouter()
router.register('movie', views.MovieView, basename='movie')
router.register('profile',views.UserProfileView,basename='profile')
router.register('review',views.ReviewView,basename='reviews')

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('token/', ObtainAuthToken.as_view()),
] + router.urls