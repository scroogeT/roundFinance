from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^account_history/', views.account_history, name="history"),
]