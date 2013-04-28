from django.contrib import admin

from {{ project_name }} import models
from sorl.thumbnail.admin import AdminImageMixin

#class FooAdmin(AdminImageMixin, admin.ModelAdmin): pass
#admin.site.register(models.Foo, FooAdmin)
