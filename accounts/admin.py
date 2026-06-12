from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    #voglio mostrare 'role' quando modifico un utente esistente...
    fieldsets = UserAdmin.fieldsets + (
        ('Ruolo Personale', {'fields': ('role',)}),
    )

    #... e quando ne creo uno da zero
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Ruolo Personale', {'fields': ('role',)}),
    )


#registro il modello usando la configurazione personalizzata
admin.site.register(CustomUser, CustomUserAdmin)