from django.urls import path
from .views import advert_create, advert_update, advert_list, advert_detail, bidding_view

app_name = 'advposts'

urlpatterns = [
    path('',advert_list.as_view(), name='adv-list'),
    path('detail/<uuid:tender_id>',advert_detail.as_view(), name='adv-detail'),
    path('new/', advert_create, name='advert-create'),
    path('update/<uuid:tender_id>/', advert_update.as_view(), name='advert-update'),
    path('bid/<uuid:tender_id>', bidding_view.as_view(), name='bid')
]