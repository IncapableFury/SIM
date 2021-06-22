from django import forms
from .models import Item, STATUS_CHOICES
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet


class ItemForm(forms.Form):

    def get_item_list():
        iquery = Item.objects.values_list('name', 'stock')
        iquery_choices = [('', 'None')] + [(name, name + " | " + str(stock)) for (name, stock) in iquery]
        return iquery_choices

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        print("wtf is going on", quantity)
        if not quantity:
            return self.fields['quantity'].initial
        return quantity

    # item = forms.ChoiceField(label="item", widget=forms.Select(attrs={'class': 'form-select', "required": "true"}),
    #                          choices=iquery_choices)
    item = forms.ChoiceField(label="item", widget=forms.Select(
        attrs={'class': 'js-example-basic-single form-control', "style": "width:auto;"}),
                             choices=get_item_list, required=False)
    quantity = forms.IntegerField(label='quantity',
                                  widget=forms.NumberInput({'min': 1}),
                                  required=True, initial=1)
    offset = forms.DecimalField(label="Offset", widget=forms.NumberInput({}), initial=0.0, required=False, )
    not_consume_inventory = forms.BooleanField(label='not_consume_inventory',
                                           help_text="Set this to True will prevent it form consuming your inventory.",
                                           initial=False,required=False)



class ItemFormSet(BaseFormSet):
    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        form.fields['item'].label = str(i + 1)
        return form

    def clean(self):
        super(ItemFormSet, self).clean()
        item_names = set()
        for form in self:
            if not form.cleaned_data:
                continue
            # print("testing", form.cleaned_data)
            item_name = form.cleaned_data['item'] if 'item' in form.cleaned_data else None
            if item_name in item_names:
                raise ValidationError("You shouldn't have two identical items in an order.")
            else:
                if item_name:
                    item_names.add(item_name)


class OrderForm(forms.Form):
    buyer = forms.CharField(label="Buyer", max_length=10,
                            widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    shipping_address = forms.CharField(label="Shipping Address", max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    tracking_number = forms.CharField(label="Tracking Number", max_length=100,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(label="Description", max_length=100,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}), required=False)
    status = forms.ChoiceField(label="Status", widget=forms.Select(attrs={'class': 'form-select'}),
                               choices=STATUS_CHOICES)


ItemFormset = forms.formset_factory(ItemForm, formset=ItemFormSet, extra=0, min_num=1, validate_min=True)


class UploadFileForm(forms.Form):
    behavior = forms.ChoiceField(label="Mode", widget=forms.Select(attrs={'class': 'form-select'}),
                                 choices=[('append', 'append'), ('override', 'override')])
    file = forms.FileField()
