from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Dataset,name="face"),

    path('detection',views.detection,name="detection"),
]