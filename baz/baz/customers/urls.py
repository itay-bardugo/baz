from django.urls import path

from . import views

urlpatterns = [
    path('sendmail', views.sendmail, name='index'),
]