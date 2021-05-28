from django import forms
from .models import Item, STATUS_CHOICES
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet


class ItemForm(forms.Form):
    iquery = Item.objects.values_list('name', flat=True).distinct()
    iquery_choices = [('', 'None')] + [(name, name) for name in iquery]
    # item = forms.ChoiceField(label="item", widget=forms.Select(attrs={'class': 'form-select', "required": "true"}),
    #                          choices=iquery_choices)
    item = forms.ChoiceField(label="item", widget=forms.Select(
        attrs={'class': 'js-example-basic-single form-control', "style": "width:auto;", "required": "true"}),
                             choices=iquery_choices)
    quantity = forms.IntegerField(label='quantity', widget=forms.NumberInput({'min': 1, "required": "true"}),
                                  required=True)


#
#
class ItemFormSet(BaseFormSet):
    def clean(self):
        super(ItemFormSet, self).clean()
        item_names = set()
        for form in self:
            if not form.cleaned_data:
                continue
            print("testing", form.cleaned_data)
            item_name = form.cleaned_data['item']
            if item_name in item_names:
                raise ValidationError("You shouldn't have two identical items in an order.")
            else:
                item_names.add(item_name)


class OrderForm(forms.Form):
    shipping_address = forms.CharField(label="Shipping Address", max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", max_length=100,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}))
    status = forms.ChoiceField(label="Status", widget=forms.Select(attrs={'class': 'form-select'}),
                               choices=STATUS_CHOICES)


ItemFormset = forms.formset_factory(ItemForm, formset=ItemFormSet, extra=0, min_num=1, max_num=9, validate_min=True)
