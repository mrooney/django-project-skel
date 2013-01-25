from coffin.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

app_urls = (
    url(r'^%s/'%name, '{{project_name}}.views.%s'%name, name=name) for name in (
        'login',
        'logout',
        'signup',
        'account',
    )
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', '{{project_name}}.views.home', name="home"),
    url(r'^email/confirm/(?P<token>[\w-]{36})/$', '{{project_name}}.views.email_confirm', name="email_confirm"),

    *app_urls
)
