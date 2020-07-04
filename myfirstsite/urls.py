from django.contrib import admin
from django.urls import path
from myfirstapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('artists', views.artists),
    path('albums', views.albums),
    path('tracks', views.tracks),
    path('genres', views.genres),
    path('topten', views.topTen),
    path('contact', views.contact),
    path('ajax/rated', views.rated),
    path('ajax/addTrack', views.addTrack),
    path('contribute', views.contribute),
]
