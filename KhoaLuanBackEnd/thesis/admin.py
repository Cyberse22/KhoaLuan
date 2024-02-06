from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.contrib.auth.models import Permission, Group, User
from django.utils.safestring import mark_safe

from .models import CustomUser, DefenseCouncil, Thesis, ThesisScore
from django.urls import path


class ThesisAppAdminSite(admin.AdminSite):
    site_header = 'Quản Lý Khóa Luận'


admin_site = ThesisAppAdminSite(name='myadmin')


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'is_active']
    list_filter = ['id', 'username']
    search_fields = ['id', 'first_name', 'last_name']
    readonly_fields = ['avatar']

    def avatar_image(self, obj):
        return mark_safe(
            '<img src="static/{url}" width="120" />'.format(url=obj.image.name)
        )


admin_site.register(CustomUser, UserAdmin)
admin_site.register(DefenseCouncil)
admin_site.register(Thesis)
admin_site.register(ThesisScore)
admin_site.register(Permission)
admin_site.register(Group)
admin_site.register(User)
