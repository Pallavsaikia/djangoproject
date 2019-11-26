from django.conf.urls import url
from dashboard_app import views

urlpatterns = [
    url(r'^$', views.Dashboard.as_view(),name='dashboard'),
]
