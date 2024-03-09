from django.contrib import admin
from django.urls import path, include
from accounts.views import home 

urlpatterns = [
    path('',home),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
