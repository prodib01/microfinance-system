from django.contrib import admin
from .models import Branch


class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "manager")
    list_filter = ("name",)
    search_fields = ("name", "location")
    list_per_page = 20


admin.site.register(Branch, BranchAdmin)
