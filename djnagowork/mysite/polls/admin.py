from django.contrib import admin
from polls.models import Poll
from polls.models import Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

#PollAdmin Class
class PollAdmin(admin.ModelAdmin):
    list_filter=['pub_date']
    search_fields = ['question']	
    list_display = ('question', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]




# Register your models here.
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)