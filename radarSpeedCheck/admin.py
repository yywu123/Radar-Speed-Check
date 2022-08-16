from django.contrib import admin

# Register your models here.

from .models import TimeSheet, CheckItem


admin.site.register(CheckItem)
admin.site.register(TimeSheet)