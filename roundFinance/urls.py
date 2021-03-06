"""roundFinance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from public import views as public_views
from dash import views as dash_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dash/', dash_views.index, name="dashboard"),
    url(r'^$', public_views.home, name="home"),
    url(r'^contact/$', public_views.contact, name="contact"),
    url(r'^about/$', public_views.about, name="about"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^signup/$', public_views.signup, name='signup'),
    url(r'^profile/', dash_views.profileView.as_view(), name="profile"),
    url(r'^(?P<member_pk>\d+)/edit$', dash_views.updateProfile.as_view(), name="editProfile"),
    url(r'^borrowerProfile/', dash_views.borrowerProfile, name="borrowerProfile"),
    url(r'^borrowerList/', dash_views.borrowerList, name="borrowerList"),
    url(r'^borrowerFunds/', dash_views.newDebt.as_view(), name="borrowFunds"),

    url(r'^creditDetail/(?P<pk>\d+)/$', dash_views.creditDetail, name="creditDetail"),

    url(r'^paybackDebt1/(?P<trans_pk>\d+)/$', dash_views.debtPayment.as_view(), name="debtPayment"),
    url(r'^receivePayment/(?P<trans_pk>\d+)/$', dash_views.receivePayment.as_view(), name="receivePayment"),

    url(r'^account_history/', dash_views.account_history, name="history"),
    url('^', include('django.contrib.auth.urls')),
]
