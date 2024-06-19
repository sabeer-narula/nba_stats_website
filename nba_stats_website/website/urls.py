from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('overpaid/', views.overpaid, name='overpaid'),
    path('highest/', views.highest, name='highest'),
    path('underpaid/', views.underpaid, name='underpaid'),
]