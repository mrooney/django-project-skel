from coffin.conf.urls import *
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

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

    url(r'^password_reset$', '{{project_name}}.views.password_reset', kwargs={'template_name': 'password_reset_form.jinja', 'post_reset_redirect': reverse_lazy('password_reset_done'), 'email_template_name': 'password_reset_email.html'}, name="password_reset"),
    url(r'^password_reset/done$', '{{project_name}}.views.password_reset_done', name="password_reset_done"),
    url(r'^reset(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', kwargs={'template_name': 'password_reset_confirm.html'}),
    url(r'^reset/done$', 'django.contrib.auth.views.password_reset_complete', kwargs={'template_name': 'password_reset_complete.html'}),

    url(r'^$', '{{project_name}}.views.home', name="home"),
    url(r'^email/confirm/(?P<token>[\w-]{36})/$', '{{project_name}}.views.email_confirm', name="email_confirm"),

    *app_urls
)
