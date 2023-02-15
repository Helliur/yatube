from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('author/', views.AboutAuthorView, name='author'),
    path('tech/', views.AboutTechView, name='tech'),
]
