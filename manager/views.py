from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.forms import formset_factory

from .models import Item
from .forms import OrderForm, ItemFormset

# Create your views here.
class view_inventory(ListView):
    model = Item
    context_object_name = "inventory"

    def get_template_names(self):
        return "item_list.html"


# def view_inventory(request):
#     inventory = Item.objects.all()
#     template = loader.get_template('item_list.html')
#     context = {
#         'inventory': inventory
#     }
#     return HttpResponse(template.render(context,request))

class view_item_detail(DetailView):
    model = Item
    context_object_name = "item_detail"
    def get_template_names(self):
        return "item_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# def view_item_detail(request, item_id):
#     item_detail = get_object_or_404(Item, pk=item_id)
#     return render(request, 'item_detail.html', {'item_detail':item_detail})

def orders(request):
    if request.method == 'POST':
        if 'additems' in request.POST and request.POST['additems'] == 'true':
            print("we are good")
            formset_dict_copy = request.POST.copy()
            formset_dict_copy['form-TOTAL_FORMS'] = int(formset_dict_copy['form-TOTAL_FORMS']) + 1
            formset = ItemFormset(formset_dict_copy)
            form = OrderForm(request.POST)
            context = {
                'form': form,
                'formset': formset
            }
            return render(request, 'create_order.html', context)
        else:
            form = OrderForm(request.POST)
            formset = ItemFormset(request.POST)
            items_list = []
            # print(form.is_valid(), formset.is_valid())
            # print(formset)
            if form.is_valid() and formset.is_valid():
                shipping_address = form.cleaned_data['shipping_address']
                description = form.cleaned_data['description']
                print(formset)
                for f in formset:
                    print(f)
                    # item = f.item
                    # quantity = f.quantity
                    items_list.append(f.cleaned_data)
                # print("-------------------", shipping_address, description, items_list)
            return render(request, "test.html", {'info':form.cleaned_data, 'info2':items_list})
    return render(request, "order_list.html", {'info':"Viewing all orders"})

def test(request):
    return render(request, 'test.html')

# render the form
def order_create(request):
    print("----------testing---------------",request.POST)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = ItemFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            shipping_address = form.cleaned_data['shipping_address']
            description = form.cleaned_data['description']
            items_list = []
            for f in formset:
                item = formset.cleaned_data['item']
                quantity = f.cleaned_data['quantity']
                items_list.append((item,quantity))
            # print("-------------------", shipping_address, description, items_list)
            return render(request, "test.html", {'info':form.cleaned_data, 'info2':formset.cleaned_data})
    else:
        form = OrderForm(initial={'Shipping Address':"test string"})
        formset = ItemFormset()
    context={
        'form': form,
        'formset': formset
    }
    return render(request, 'create_order.html', context)

def test_order(request):
    print(request)
    pass
