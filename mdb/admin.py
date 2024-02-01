from django.contrib import admin

# Register your models here.
from mdb.models import Genre,Movie,UserProfile,Language

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(UserProfile)
admin.site.register(Language)