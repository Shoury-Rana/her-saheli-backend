from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    # --- Configuration for the User List View in Admin ---
    list_display = ('email', 'is_staff', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)

    # --- Configuration for the User EDIT page ---
    # This was corrected in the previous step.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # --- Configuration for the User ADD page (THE FIX) ---
    # This was missing. We must define it to override the default which expects 'username'.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'), # Replaced 'username' with 'email'
        }),
    )

    inlines = (UserProfileInline,)

admin.site.register(User, CustomUserAdmin)