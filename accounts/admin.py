from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import AccountUser

class AccountAdmin(UserAdmin):
    list_display    = ('email', 'first_name', 'mobNo', 'last_login', 'is_orgadmin', 'is_staff', 'is_bidder',)
    search_fields   = ('email','mobNo','aadhaarNo',)
    readonly_fields = ('date_joined','last_login',)
    ordering = ['email',]
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

admin.site.register(AccountUser, AccountAdmin)
