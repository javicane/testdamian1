"""sierradjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,  include
from sierraapp import views
from core.views import front, note, note_detail

urlpatterns = [
    path('sierraapp/', include('sierraapp.urls')),
    path('admin/', admin.site.urls),
    path('naver/', views.naver, name='naver'),
    path('upload_new_app/', views.upload_view, name='upload'),
    path('choose_masking_engine/', views.choose_masking_engine_view, name='choose_masking_engine'),
    path('create_mj/', views.create_mj_view, name='create_mj'),
    path("", front, name="front"),
    path("notes/", note, name="note"),
    path("notes/<int:pk>/", note_detail, name="detail"),
]
