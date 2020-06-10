from django.contrib import admin
from org.models import Org, OrgUser, OrgOwner
from organizations.models import (Organization, OrganizationUser,
    OrganizationOwner)

class OrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','created_by',]
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name']
# class OrgAdmin(BaseOrganizationUserAdmin):

admin.site.unregister(Organization)
admin.site.unregister(OrganizationUser)
admin.site.unregister(OrganizationOwner)
admin.site.register(Org, OrgAdmin)
admin.site.register(OrgUser)
admin.site.register(OrgOwner)
