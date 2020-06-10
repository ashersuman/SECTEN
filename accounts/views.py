from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import PermissionDenied
from invitations.views import AcceptInvite
from invitations.signals import invite_accepted
from django.dispatch import receiver
from invitations.models import Invitation
from org.models import OrgUser
from accounts.forms import RegistartionForm, UserAuthenticationForm, AccountUpdateForm
# from org.forms import OrgMemberRegistrationForm

# Create your views here.
class signup_view(TemplateView):
    template_name = 'registration/signup.html'

def signup_bidder_view(request):
    context = {}
    if request.POST:
        form = RegistartionForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=password)
            login(request, account)
            return redirect('home')
        else:
            context['bidder_form'] = form
    else:
        form = RegistartionForm()
        context['bidder_form'] = form
        context['type'] = 'Bidder'

    return render(request, 'accounts/signup_bidder.html', context)

def signup_orgadmin_view(request):
    context = {}
    if request.POST:
        form = RegistartionForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.is_bidder = False
            instance.is_orgadmin = True
            instance.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=password)
            login(request, account)
            return redirect('org:orgregister')
        else:
            context['bidder_form'] = form
    else:
        form = RegistartionForm()
        context['bidder_form'] = form
        context['type'] = 'Admin'

    return render(request, 'accounts/signup_bidder.html', context)
'''
    :Todo:
    #using class based view to eliminate the use of global variable
    :    :
'''
_invite_email = None
@receiver(invite_accepted)
def getemail(email, **kwargs):
    global _invite_email
    _invite_email = email

def signup_member_view(request):
    global _invite_email
    if _invite_email != None:
        invite = Invitation.objects.filter(email=_invite_email).first()
        invitee_org = OrgUser.objects.filter(user_id=invite.inviter_id).first()
    # print("inviter_id: ",invite.inviter_id)
    # print("ORG: ", invitee_org.organization_id)
    # print("GOT EMAIL VIA RECEIVER: " ,invite_email)
    context = {}
    if request.POST:
        form = RegistartionForm(request.POST)
        if invitee_org.is_admin:
            if form.is_valid() and request.POST.get('email','') == _invite_email:
                instance = form.save()
                instance.is_bidder = False
                instance.is_staff = True
                instance.save()
                member = OrgUser.create(instance.id, invitee_org.organization_id, False)
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=password)
                login(request, account)
                _invite_email = None
                return redirect('home')
            else:
                if(request.POST.get('email','') != _invite_email):
                    context['troll'] = 'Woah! You got some skills! (Invite Email Mismatch)'
                context['member_form'] = form
        else:
            context['admin_error'] = 'Sorry we can\'t resgister you. Ask your admin to send a request!'
    else:
        if _invite_email == None:
            raise PermissionDenied()
        else:
            form = RegistartionForm(initial={'email':_invite_email})
            context['member_form'] = form
            context['invited_mail'] = _invite_email
    return render(request, 'accounts/signup_trust.html', context)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                if user.is_superuser:
                    print('Baap re Baap SuperUserwa')
                if user.is_bidder:
                    print('Bidder Kia h Login')
                if user.is_orgadmin:
                    print('Bade log Admin Bhaiya')
                if user.is_staff:
                    print('Staff chi chi.')
                
                return redirect('home')
    else:
        form = UserAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def account_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "mobNo": request.user.mobNo,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )
    
    context['account_form'] = form
    return render(request, 'accounts/account.html', context)

