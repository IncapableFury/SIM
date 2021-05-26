from django import forms


class OrderForm(forms.Form):
    shipping_address = forms.CharField(label="Shipping Address", max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", max_length=100,
                                       widget=forms.Textarea(attrs={'class': 'form-control','rows':"3"}))
