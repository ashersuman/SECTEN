from django import forms
from org.models import Org, OrgUser,OrgOwner
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from organizations.backends import invitation_backend
from invitations.utils import get_invitation_model
from django.urls import reverse
from django.core.exceptions import ValidationError

class OrgRegistrationForm(forms.ModelForm):
    class Meta:
        model = Org
        fields = [
            'name',
            'location',
            'slug',
        ]

class OrgOwnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = OrgOwner
        exclude = ['organization_user_id','organization_id']

# class OrgMemberRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = OrgUser
#         fields = ['User']
class InviteMemberForm(forms.Form):
    email = forms.EmailField() 

    def __init__(self, *args, **kwargs):
        self.invite_url = None
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        try:
            user = self.request.user
            Invitation = get_invitation_model()
            invite = Invitation.create(self.cleaned_data["email"], inviter=self.request.user)
            invite.send_invitation(self.request)
            invite_url = reverse('invitations:accept-invite', args=[invite.key])
            invite_url = self.request.build_absolute_uri(invite_url)
            self.invite_url = invite_url
            return self.cleaned_data
        except:
            import sys
            raise ValidationError(sys.exc_info())

    def save(self, **kwargs):
        pass