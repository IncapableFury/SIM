from django import forms
from .models import Item


class ItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all().values_list('name', flat=True))
    quantity = forms.IntegerField(label='quantity')

class OrderForm(forms.Form):
    shipping_address = forms.CharField(label="Shipping Address", max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", max_length=100,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}))
    status = forms.ChoiceField(label="Status", widget=forms.Select(attrs={'class': 'form-select'}),
                               choices=[('1', 'First'), ('2', 'Second')])
    # items = forms.ModelChoiceField(queryset=Item.objects.all().values_list('name', flat=True))
    # item = forms.formset_factory(ItemForm, extra=3)


ItemFormset = forms.formset_factory(ItemForm, extra=1)

