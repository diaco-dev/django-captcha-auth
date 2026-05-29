
from user.models import CustomUser
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser

@admin.register(CustomUser)
class UserResource(ImportExportModelAdmin):
    resource_class = UserResource

#
# class UserManagerResource(resources.ModelResource):
#     class Meta:
#         model = UserManager
#
#
# @admin.register(UserManager)
# class UserManagerResource(ImportExportModelAdmin):
#     resource_class = UserManagerResource
