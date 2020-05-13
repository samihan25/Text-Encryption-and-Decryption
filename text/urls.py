from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('serve_request', views.serve_request, name='serve_request'),
]