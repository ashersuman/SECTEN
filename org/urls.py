from django.urls import path
from .views import OrgRegistrationView, InviteMember

app_name = 'org'

urlpatterns = [ 
    path('register/', OrgRegistrationView, name='orgregister'),
    path("invite/", InviteMember.as_view(), name="invite_member")
]