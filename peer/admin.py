from django.contrib import admin

from models import Paper

class PaperAdmin(admin.ModelAdmin):
    date_hierarchy = "submitted"
    list_display = ("title", "author", "published")

admin.site.register(Paper, PaperAdmin)
