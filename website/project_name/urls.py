from coffin.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', '{{project_name}}.views.home', name="home"),
    url(r'^login/', '{{project_name}}.views.login', name="login"),
    url(r'^logout/', '{{project_name}}.views.logout', name="logout"),
    url(r'^signup/', '{{project_name}}.views.signup', name="signup"),
)
