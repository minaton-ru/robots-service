from django.contrib import admin

from .models import Robot


class RobotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Robot, RobotAdmin)
