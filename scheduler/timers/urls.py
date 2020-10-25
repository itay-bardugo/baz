from django.urls import path
from django.conf.urls import url


from . import views

urlpatterns = [
    path('create', views.new, name='new'),
    url(r'^(?P<signature>.+)/stop/$', views.stop, name='stop'),
]