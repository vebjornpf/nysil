from django.contrib import admin

from.models import Subject, Chapter, Exercise_Page




class SubjectAdmin(admin.ModelAdmin):
    # doing this to make the Subject-table more transparent for the admins
    search_fields = ['subject_code']
    list_display = ('subject_code', 'subject_name', 'get_full_name')


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['get_number_and_name','subject']
    ordering = ['subject', 'chapter_number']

class Exercise_PageAdmin(admin.ModelAdmin):
    list_display = ['headline']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Exercise_Page, Exercise_PageAdmin)
