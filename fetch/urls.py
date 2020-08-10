from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('callback/', views.callback, name='callback'),
    path('request/', views.request, name='request'),
]
