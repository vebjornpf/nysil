from django.contrib import admin

from.models import Subject, Theme, Exercise_Page




class SubjectAdmin(admin.ModelAdmin):
    # doing this to make the Subject-table more transparent for the admins
    search_fields = ['subject_code']
    list_display = ('subject_code', 'subject_name', 'get_full_name')


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['get_number_and_name','subject']
    ordering = ['subject', 'chapter_number']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Theme, ThemeAdmin)