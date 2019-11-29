from django.conf.urls import url
from api import views

urlpatterns = [
    # url(r'^$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^register/', views.RegisterApiView.as_view(), name='register')

]
