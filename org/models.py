from django.db import models
from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationOwner,
    AbstractOrganizationUser
)
from invitations.models import AbstractBaseInvitation
from django.contrib.auth import get_user_model

class Org(AbstractOrganization):
    name        = models.CharField(max_length=100)
    slug        = models.CharField(max_length=150)
    location    = models.CharField(max_length=300, default = None, null=True, verbose_name='Address')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey(get_user_model(), models.CASCADE, blank=True, null=True, verbose_name='Owner/Combiner')
    
    def __str__(self):
        return self.name

    @classmethod
    def get(cls, name):
        org = Org.objects.get(name=name)
        return org

    class Meta:
        verbose_name = 'Organisation'

class OrgUser(AbstractOrganizationUser):
    class Meta:
        verbose_name = "Member"

    @classmethod
    def create(cls, user, org, admin):
        org_user = cls(user_id = user, organization_id=org, is_admin=admin)
        org_user.save()
        return org_user

class OrgOwner(AbstractOrganizationOwner):
    class Meta:
        verbose_name = "Combiner"

    @classmethod
    def create(cls, user, org):
        org_owner = cls(organization_user_id = user, organization_id=org)
        org_owner.save()
        return org_owner 
    @classmethod
    def get_orgid(cls,user_id):
        orgid = OrgOwner.objects.get(organization_user_id=user_id)
        return orgid