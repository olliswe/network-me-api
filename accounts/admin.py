from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Category


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id','name')
#     list_display_links = ('id','name',)
#     list_per_page = 25
#
# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('first_name', 'last_name','email','organization', 'admin','staff','category')
#     list_display_links = ('first_name', 'last_name','email')
#     list_filter = ('division',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name','last_name','organization','category')}),
#         ('Permissions', {'fields': ('admin','staff')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name','last_name','position','division','password1', 'password2')}
#         ),
#     )
#     search_fields = ('email','first_name','last_name')
#     ordering = ('last_name',)
#     filter_horizontal = ()


admin.site.register(User)
admin.site.register(Category)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)