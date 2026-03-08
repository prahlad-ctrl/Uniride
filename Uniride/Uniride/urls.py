"""
URL configuration for Uniride project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sign_up, name='signup'),
    path('login/',login_page,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('show_rides/', show_rides, name='show_rides'),
    path('profile/',profile,name='profile'),
    path('logout/', logout, name='logout'),
    path('post_ride/', post_ride, name='post_ride'),
    path('register_vehicle/', publish_vehicle, name='register_vehicle'),
    path('riders_profile/<int:ride_id>/', rider_profile, name='rider_profile')
]
