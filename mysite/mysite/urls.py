from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls', namespace="accounts")),
    path('admin/', admin.site.urls),
    path('portfolio/', include('portfolio.urls', namespace="portfolio")),
    path('stocks/', include('stocks.urls', namespace="stocks"))
]
admin.site.site_header = "Momentum Admin"
admin.site.site_title = "Momentum Admin Portal"
admin.site.index_title = "Welcome to Momentum Portal"