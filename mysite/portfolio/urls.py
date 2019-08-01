from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_view, name='portfolio'),
    path('about/', views.about_view, name='about')
]