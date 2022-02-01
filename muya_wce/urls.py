"""muya_wce URL Configuration"""
from django.conf.urls import include, re_path
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.staticfiles.storage import staticfiles_storage
from muya_wce.views import *

urlpatterns = [
    re_path(r'^$', main_page),
    re_path(r'favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('muya_wce/images/favicon.ico'))),
    re_path(r'^collation/', include('collation.urls')),
    re_path(r'^transcriptions/', include('transcriptions.urls')),
    re_path(r'^api/?', include('api.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'pollstate', poll_state, name="pollstate")
]

admin.site.site_header = 'MUYA Editing Tool Administration'
admin.site.index_title = 'Administration index'
admin.site.site_title = 'MUYA Editing Tools Admin'
