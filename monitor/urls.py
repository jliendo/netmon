from django.conf.urls import include, url
from django.contrib import admin

from netmon import urls as netmon_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^netmon/', include(netmon_urls)),
]
