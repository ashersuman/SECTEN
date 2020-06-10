from django import forms
from .models import AdvDetails
from flatpickr import DateTimePickerInput

class AdvertCreateForm(forms.ModelForm):
    class Meta:
        model = AdvDetails
        fields = ['title', 'dept', 'descrip', 
                  'bid_start_date', 'bid_end_date', 
                  'part_start_date', 'part_end_date', 
                  'comb_start_date', 'comb_end_date',
                  'advFile']
        widgets = {
            'descrip' : forms.Textarea(),
            'bid_start_date' : DateTimePickerInput().start_of('bids'),
            'bid_end_date' : DateTimePickerInput().end_of('bids').start_of('part'),
            'part_start_date' : DateTimePickerInput().end_of('part').start_of('share'),
            'part_end_date' : DateTimePickerInput().end_of('share').start_of('fwd'),
            'comb_start_date' : DateTimePickerInput().end_of('fwd').start_of('comb'),
            'comb_end_date' : DateTimePickerInput().end_of('comb'),
        }
        

class AdvertUpdateForm(forms.ModelForm):
    class Meta:
        model = AdvDetails
        fields = ['title', 'dept', 'descrip', 'state', 
                  'bid_start_date', 'bid_end_date', 
                  'part_start_date', 'part_end_date', 
                  'comb_start_date', 'comb_end_date',
                  'advFile']
        widgets = {
            'descrip' : forms.Textarea(),
            'bid_start_date' : DateTimePickerInput().start_of('bids'),
            'bid_end_date' : DateTimePickerInput().end_of('bids').start_of('part'),
            'part_start_date' : DateTimePickerInput().end_of('part').start_of('share'),
            'part_end_date' : DateTimePickerInput().end_of('share').start_of('fwd'),
            'comb_start_date' : DateTimePickerInput().end_of('fwd').start_of('comb'),
            'comb_end_date' : DateTimePickerInput().end_of('comb'),
        }
        