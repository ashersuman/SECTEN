from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_view, name='account'),
    path('login/', views.login_view,name='login'),
    path('signup/', views.signup_view.as_view(), name='signup'),
    path('signup/bidder/', views.signup_bidder_view, name='signup_bidder'),
    path('signup/member/', views.signup_member_view, name='signup_member'),
    path('signup/orgadmin/', views.signup_orgadmin_view, name='signup_orgadmin'),
    path('logout/', views.logout_view, name='logout'),
]

#action="{% url 'accounts:signup_bidder' %}"