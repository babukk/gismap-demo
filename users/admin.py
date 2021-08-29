
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(UserAdmin):

    # Указываем django использовать формы (из forms.py):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('login',)
    list_filter = ('login',)
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2',)}
        ),
    )
    search_fields = ('login',)
    ordering = ('login',)

admin.site.register(User, UserAdmin)
