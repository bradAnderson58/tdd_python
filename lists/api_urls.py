
from django.conf.urls import url
from lists import api


urlpatterns = [
    url(r'^lists/(\d+)/$', api.lists, name='api_list')
]