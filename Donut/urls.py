"""Donut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import (
    path,
    include
)
from donut_app import views

urlpatterns = [
    path('admin/',
admin.site.urls),
    path('',
views.DonutListView.as_view()),
#     path('cart/',
# views.),
    path('donut/<int:pk>',
views.DonutDetailView.as_view()),
#     path('payment/ ',
# views.),
    path('api/',
include('donut_app.urls')),
]
