from django.contrib import admin
from flag.models import FlaggedContent, FlagInstance

class InlineFlagInstance(admin.TabularInline):
    model = FlagInstance
    extra = 0

class FlaggedContentAdmin(admin.ModelAdmin):
    list_display        = ('content_object', 'creator', 'status',
                           'moderator', 'count')
    list_filter = ["status",'moderator']
    inlines = [InlineFlagInstance]

admin.site.register(FlaggedContent, FlaggedContentAdmin)
