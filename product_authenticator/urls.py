"""product_authenticator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authenticate.views import authenticate, get_csv, view_test_result
import admin_honeypot
from django.urls import include

urlpatterns = [
    path("dont-try-this/", admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='honeypot')),
    path('authenticate', authenticate, name="authenticate"),
    path('generate/csv', get_csv, name="generatecsv"),
    path('test-result', view_test_result, name="view_test_result" )
]


admin.site.site_header = "VerifyInnocent Admin"
admin.site.site_title = "VerifyInnocent admin Portal"
admin.site.index_title = "Welcome to Innocent Authentication Portal"