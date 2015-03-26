from django.contrib import admin

# Register your models here.
from first.models import *

admin.site.register(Entity)
admin.site.register(ExtensionDefinition)
admin.site.register(ExtensionRecord)
admin.site.register(Alias)
admin.site.register(States)




