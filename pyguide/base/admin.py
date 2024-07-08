from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

from .models import  Class_room , User_extension , Material , Student_material , Exec_core , Exec_error_log , Series_log , Error_map_table


admin.site.register(Class_room)
admin.site.register(User_extension)
admin.site.register(Material)
admin.site.register(Student_material)
admin.site.register(Exec_core)
admin.site.register(Exec_error_log)
admin.site.register(Series_log)
admin.site.register(Error_map_table)

class User_extension_Inline(admin.StackedInline):
    model = User_extension
    can_delete = False
    verbose_name_plural = 'user_extension'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (User_extension_Inline,)
    list_display = ('username','first_name','last_name','is_staff','get_identity','get_class_room','get_experimental_group')
    def get_experimental_group(self, obj):
        return obj.user_extension.experimental_group
    get_experimental_group.short_description = 'experimental_group'
    def get_identity(self, obj):
        return obj.user_extension.login_identity
    get_identity.short_description = 'login_identity'
    def get_class_room(self, obj):
        return obj.user_extension.class_room
    get_class_room.short_description = 'class_room'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)