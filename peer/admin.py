from django.contrib import admin

from models import Paper, Review, Revision

class PaperAdmin(admin.ModelAdmin):
    date_hierarchy = "submitted"
    list_display = ("title", "author", "published")


class ReviewAdmin(admin.ModelAdmin):
    date_hierarchy = "submitted"
    list_display = ("paper", "author", "decision")


class RevisionAdmin(admin.ModelAdmin):
    date_hierarchy = "submitted"
    list_display = ("paper", "submitted")

admin.site.register(Paper, PaperAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Revision, RevisionAdmin)
