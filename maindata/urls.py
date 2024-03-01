from django.contrib import admin
from django.urls import include, path

from .views import createvisitforreserve,addpaid,getactivevisiturl
app_name = 'maindata'

urlpatterns = [
    path('createvisitforreserve/<int:pk>/', createvisitforreserve, name='createvisitforreserve'),
    path('addpaid/<int:pk>/', addpaid, name="addpaid"),
    path('getactivevisiturl/', getactivevisiturl, name="getactivevisiturl"),
]



