from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Sympathie
from .forms import MyUserCreationForm, MyUserChangeForm

class MyUserAdmin(UserAdmin):
    model = MyUser
    add_form = MyUserCreationForm
    list_display = ('email', 'last_name', 'first_name',)
    ordering = ('last_name', 'first_name',)
    fieldsets = (
        (None, {"fields": ('email', 'first_name', 'last_name', 'gender', 'photo', 'password')}),
        (
            ("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Даты"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('last_name', 'first_name', 'email', 'gender', 'photo', 'password1', 'password2'),
            },
        ),
    )
    form = MyUserChangeForm
    # change_password_form = AdminPasswordChangeForm
    list_filter = ("last_name", "gender", "is_staff", "groups")
    search_fields = ("first_name", "last_name", "email", "gender")
    ordering = ("last_name", "first_name",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

class SympathieAdmin(admin.ModelAdmin):
    model = Sympathie

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Sympathie, SympathieAdmin)