from coffin.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', '{{ project_name.views.home }}'),
    # there's a login one too that takes a template
    url(r'^logout/', 'django.contrib.auth.views.logout'),
)
