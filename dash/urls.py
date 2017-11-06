from django.conf.urls import url
from django.contrib import admin
import roundFinance.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]