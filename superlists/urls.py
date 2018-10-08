
from django.conf.urls import url, include
from lists import views as list_views
from lists import urls as list_urls
from accounts import urls as account_urls
#from lists import api_urls
from lists.api import router

urlpatterns = [
    url(r'^$', list_views.HomePageView.as_view(), name='home'),
    url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(account_urls)),
    #url(r'^api/', include(api_urls)),
    url(r'^api/', include(router.urls)),
]
