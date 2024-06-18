"""
URL configuration for kavlingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from dashboard import urls as dashboard_urls
from kavling import urls as kavling_urls
from marketing import urls as marketing_urls
from customer import urls as customer_urls
from user import urls as user_urls
from website import urls as site_urls

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',  include(dashboard_urls)),
    path('',  include(kavling_urls)),
    path('',  include(marketing_urls)),
    path('',  include(customer_urls)),
    path('',  include(user_urls)),
    path('',  include(site_urls)),
]

handler404 = 'kavling.views.custom_404'