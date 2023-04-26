from django.urls import path
from . import views

urlpatterns = [
    
   path('', views.sec, name='sec'),
   path('recherche', views.recherche, name='recherche'),
    
]
