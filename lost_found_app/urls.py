from django.urls import path, include
from django.contrib import admin
from .views import hello_world

urlpatterns = [
    path('hello/', hello_world),
]
