from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from org.models import Org, OrgUser
from advposts.forms import AdvertCreateForm,AdvertUpdateForm
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse
from .models import AdvDetails
from django.http import Http404
from django.core.exceptions import PermissionDenied

# Create your views here.
def home_view(request):
    return render(request,'advposts/home.html')

def advert_create(request):
    context = {}
    if request.method == "POST":
        form = AdvertCreateForm(request.POST, request.FILES)
        print('Request? ', request.FILES)
        print('User ID? ', request.user.id)
        print('Org ? ', OrgUser.objects.filter(user_id=request.user.id).first())
        if form.is_valid():
            print('FORM: ',form)
            instance = form.save(commit=False)
            instance.advFile = request.FILES['advFile']
            instance.author = request.user
            org_id = OrgUser.objects.filter(user_id=request.user.id).first().organization_id
            instance.organisation = Org.objects.get(id = org_id)
            instance.save()
            return redirect('home')
        else:
            context['form'] = form
    else:
        if not request.user.is_orgadmin:
            raise PermissionDenied
        form = AdvertCreateForm()
        context['form'] = form
    return render(request, 'advposts/advert_create_form.html', context)

class advert_update(SuccessMessageMixin, UpdateView):
    template_name = 'advposts/advert_update_form.html'
    form_class = AdvertUpdateForm
    model = AdvDetails
    pk_url_kwarg = 'tender_id'
    success_message = 'Updated Successfully'

    def get_success_url(self):
        return reverse('advposts:advert-update',kwargs={'tender_id' : self.kwargs['tender_id']})
    
    def get_object(self, *args, **kwargs):
        obj = super(advert_update, self).get_object(*args, **kwargs)
        if not obj.author == self.request.user:
            raise PermissionDenied
        return obj

class advert_list(TemplateView):
    template_name = 'advposts/adv_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advs'] = AdvDetails.objects.all()[:5]
        return context

class advert_detail(TemplateView):
    template_name = 'advposts/adv_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adv_detail'] = AdvDetails.objects.get(pk=self.kwargs['tender_id'])
        context['org'] = OrgUser.objects.filter(organization=context['adv_detail'].organisation).values_list('user',flat=True)
        return context

class bidding_view(CreateView):
    pass
