from django.conf.urls import url

from views import NetMonView, CDPView, DHCPView, LLDPView
from views import DNSView, PingView, TraceView

urlpatterns = [
    url(
        r'^$',
        NetMonView.as_view(),
        name='netmon_view',
    ),
    url(
        r'cdp/$',
        CDPView.as_view(),
        name='cdp_view',
    ),
    url(
        r'lldp/$',
        LLDPView.as_view(),
        name='lldp_view',
    ),
    url(
        r'dhcp/$',
        DHCPView.as_view(),
        name='dhcp_view',
    ),
    url(
        r'dns/$',
        DNSView.as_view(),
        name='dns_view',
    ),
    url(
        r'ping/$',
        PingView.as_view(),
        name='ping_view',
    ),
    url(
        r'trace/$',
        TraceView.as_view(),
        name='trace_view',
    ),
]
