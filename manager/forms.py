from django import forms
from .models import Item


class ItemForm(forms.Form):
    iquery = Item.objects.values_list('name', flat=True).distinct()
    iquery_choices = [('', 'None')] + [(name, name) for name in iquery]
    item = forms.ChoiceField(label="Item", widget=forms.Select(attrs={'class': 'form-select'}),
                             choices=iquery_choices)
    quantity = forms.IntegerField(label='quantity')


class OrderForm(forms.Form):
    shipping_address = forms.CharField(label="Shipping Address", max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", max_length=100,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}))
    status = forms.ChoiceField(label="Status", widget=forms.Select(attrs={'class': 'form-select'}),
                               choices=[('1', 'First'), ('2', 'Second')])

ItemFormset = forms.formset_factory(ItemForm, min_num=1, max_num=9)
