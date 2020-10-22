from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.start, name='start'),
    path('listener/', views.listener, name='listener')
]
