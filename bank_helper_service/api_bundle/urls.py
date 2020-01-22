from django.conf.urls import patterns, url
from api_bundle import views
urlpatterns = patterns('',
                       url(r'^branches/autocomplete/', views.autocomplete, name=u'v1'),
                       )