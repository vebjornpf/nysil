from django.contrib import admin

from.models import Subject, Chapter, Exercise_Page, UserProfile, Comment, StudentConnectExercise, StudentConnectSubject




class SubjectAdmin(admin.ModelAdmin):
    # doing this to make the Subject-table more transparent for the admins
    search_fields = ['subject_code','subject_name']
    list_display = ('subject_code', 'subject_name', 'get_full_name')



class ChapterAdmin(admin.ModelAdmin):
    raw_id_fields = (('subject'),)
    list_display = ['get_number_and_name','subject']
    ordering = ['subject', 'chapter_number']

class Exercise_PageAdmin(admin.ModelAdmin):
    list_display = ['headline']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Exercise_Page, Exercise_PageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment)
admin.site.register(StudentConnectExercise)
admin.site.register(StudentConnectSubject)
