from django.contrib import admin
from advposts.models import AdvDetails,BidDetails
# Register your models here.

class AdvAdmin(admin.ModelAdmin):
    list_display = [
        'tenderID',       
        'title',          
        'descrip',        
        'organisation',   
        'dept',           
        'state',          
    ]
    search_fields = ['tenderID']

admin.site.register(AdvDetails, AdvAdmin)
admin.site.register(BidDetails)