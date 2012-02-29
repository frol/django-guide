from django.contrib import admin

from .models import Guide, UserGuide


class UserGuideAdmin(admin.TabularInline):
    model = UserGuide


class GuideAdmin(admin.ModelAdmin):
    inlines = [
        UserGuideAdmin,
    ]
    list_display = ('name', 'html_selector', 'visibility_mode', )

admin.site.register(Guide, GuideAdmin)
