from django.contrib import admin
from .models import ViolationInfo, Violation
import time


@admin.register(ViolationInfo)
class ViolationInfoAdmin(admin.ModelAdmin):
    """ViolationInfo class 관리"""

    list_display = (
        "name_list",
        "cctv",
        "detected_time",
    )

    def name_list(self, obj):
        return ",".join([violation.name for violation in obj.violations.all()])


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    """Violation class 관리"""

    list_display = ("name",)
