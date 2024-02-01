from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    name=models.CharField(max_length=200,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    poster = models.ImageField(upload_to="images", default="default.jpg")
    genre = models.ManyToManyField(Genre,related_name="gen")
    language=models.ForeignKey(Language,on_delete=models.CASCADE,related_name="lan")
    about=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def reviewcount(self):
        return self.r_movie.count()
    
    @property
    def reviews(self):
        return self.r_movie.all()

    def __str__(self):
        return self.title

class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="r_user")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="r_movie",null=True)
    text = models.CharField(max_length=200,blank=True)
    rating = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(5)],blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    d_name = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="profileimages", default="profile.jpg")
    dob = models.DateField(null=True)
    options = (("male", "male"), ("female", "female"))
    gender = models.CharField(max_length=200, choices=options, default="male")
    watchlist = models.ManyToManyField(Movie, blank=True, null=True, related_name="p_movie")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def reviews(self):
        return self.user.r_user.all()
    
    def __str__(self) -> str:
        return self.user.username
    

def create_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
