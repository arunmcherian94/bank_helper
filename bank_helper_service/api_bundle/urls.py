from django.conf.urls import patterns, url
from api_bundle import views
urlpatterns = patterns('',
                       url(r'^branches/autocomplete/', views.autocomplete, name=u'v1_autocomplete'),
                       url(r'^branches/', views.branch_search, name=u'v1_branch_search'),
                       )