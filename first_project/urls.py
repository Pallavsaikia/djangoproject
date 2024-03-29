"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from first_app import views
from dashboard_app import views as v

urlpatterns = [
    url(r'^$', views.Login.as_view(), name='login'),
    url(r'^logout/', views.Logout.as_view(), name='logout'),
    url(r'^dashboard/', include('dashboard_app.urls'), name='dashboard'),
    url(r'^query/(?P<value>\d+)?/?$', v.QueryViewThread.as_view(), name='query'),
    url(r'^appoint/(?P<id>\d+)?/?$', v.PendingViewThread.as_view(), name='appoint'),
    url(r'^api/', include('api.urls'), name='api'),
    path('admin/', admin.site.urls),
]
