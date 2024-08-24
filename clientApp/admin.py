from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "nationality", "phone", "gender", "created_at")
    list_filter = ("gender", "nationality")
    search_fields = ("full_name", "phone")
    list_per_page = 20


admin.site.register(Person, PersonAdmin)
