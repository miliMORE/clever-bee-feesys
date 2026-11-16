from django.urls import path

from . import views

urlpatterns = [
    path('healthz', views.healthz, name='healthz'),
    path('healthz/', views.healthz),
    path('', views.home, name='home'),
]
