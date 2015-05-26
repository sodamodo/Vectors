from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView




urlpatterns = patterns('',
    url(r'^$', 'fly.views.pretty', name='pretty'),
    url(r'pretty', 'fly.views.pretty', name='pretty'),
    url(r'converter', 'fly.views.converter', name='converter'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)