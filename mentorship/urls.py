from django.conf.urls import url
from .views import new_connection_request, \
    accept_connection, connection_detail, AllConnectionsList


app_name = 'mentorship'

urlpatterns = [
    url(r'new_connection_request$', new_connection_request, name="new_connection_request"),
    url(r'accept_connection/(?P<id>\d+)/$', accept_connection, name="accept_connection"),
    url(r'^(?P<id>\d+)/$', connection_detail, name='connection_detail'),
    url(r'^(?P<username>[-\w]+)/$', AllConnectionsList, name='user_connections'),
    url(r'all$', AllConnectionsList.as_view())
]