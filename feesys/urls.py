from django.contrib import admin
from django.urls import path, include
from core.redirects import post_login_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Auth flows
    path('accounts/profile/', post_login_redirect, name='account_profile'),
    path('accounts/', include('django.contrib.auth.urls')),
]
