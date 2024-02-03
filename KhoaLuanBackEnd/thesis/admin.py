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


admin_site.register(CustomUser)
admin_site.register(DefenseCouncil)
admin_site.register(Thesis)
admin_site.register(ThesisScore)
admin_site.register(Permission)
admin_site.register(Group)
