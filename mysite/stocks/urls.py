from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
	path('<ticker>', views.stocks_view, name='stock'),
	path('', views.stocks_view),
    path('error/', views.error_view, name='error')
]

