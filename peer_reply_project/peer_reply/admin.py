from django.contrib import admin
from peer_reply.models import University, School, Level, Course

# Add in this class to customized the Admin Interface

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    prepopulated_fields = {'slug':('name',)}

# class School_LevelAdmin(admin.ModelAdmin):
#     list_display = ('school','level' )

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')



class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')
    prepopulated_fields = {'slug':('name',)}


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    prepopulated_fields = {'slug':('name',)}

# Update the registration to include this customised interface

admin.site.register(University, UniversityAdmin)
admin.site.register(School, SchoolAdmin)
# admin.site.register(School_Level, School_LevelAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Course, CourseAdmin,)






