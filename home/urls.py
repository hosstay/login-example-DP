from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name = 'home'),
    path('/', views.Home.as_view(), name = 'home'),
    path('home/', views.Home.as_view(), name = 'home'),
    path('name/', views.Name.as_view(), name = 'name'),
    path('surf/', views.Surf.as_view(), name = 'surf'),
]