from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/rfq/(?P<rfq_id>\d+)/$', consumers.RFQConsumer.as_asgi()),
]