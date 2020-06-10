from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from org.models import *
from org.forms import InviteMemberForm, OrgRegistrationForm
from django.http import Http404


def OrgRegistrationView(request):
    context = {}
    if request.method == 'POST':
        form = OrgRegistrationForm(request.POST,instance=Org())
        print("FORM: ",form)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.created_by = request.user
            profile.save()
            print("REQUEST: ", request.user.id)
            org = Org.get(profile.name)
            print("ORGID: ", org.id)
            owner = OrgUser.create(request.user.id, org.id, True)
            comb = OrgOwner.create(owner.id, org.id)
            print("OWENER: ", owner.user)
            return redirect('home')
        else:
            context['orgregister_form'] = form
    
    else:
        form = OrgRegistrationForm()
        context['orgregister_form'] = form
    
    return render(request, 'org/orgregister.html', context)

class InviteMember(View):
    form_class = InviteMemberForm
    template_name = "org/invite_member.html"

    def get(self, request):
        if not self.request.user.is_orgadmin:
            raise Http404
        form = self.form_class(request=request)
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request=request)
        if form.is_valid():
            form.save()
            print(form)
            return render(request, 'org/invite_link.html', {"invite_link": form.invite_url, 'friend_mail': form.data['email']})

        return render(request, self.template_name, {"form": form})