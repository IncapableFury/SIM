from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.forms import formset_factory

from .models import Item, Order, OrderItems
from .forms import OrderForm, ItemFormset
from django.forms.models import model_to_dict


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
    if request.method == 'POST':  # add item row; it shouldn't be there
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
        else:  # create order
            form = OrderForm(request.POST)
            formset = ItemFormset(request.POST)
            items_list = []
            print(form.is_valid(), formset.is_valid(), formset.errors, formset.non_form_errors)
            # print(formset)
            if form.is_valid() and formset.is_valid():
                shipping_address = form.cleaned_data['shipping_address']
                description = form.cleaned_data['description']
                init_status = form.cleaned_data['status']
                new_order = Order(shipping_address=shipping_address, description=description,
                                  status=init_status)
                new_order.save()
                # print(formset)
                for f in formset:
                    item = Item.objects.get(name=f.cleaned_data["item"])
                    order_item = OrderItems(order=new_order, item=item, quantity=f.cleaned_data["quantity"])
                    # item = f.item
                    # quantity = f.quantity
                    order_item.save()
                    items_list.append(f.cleaned_data)
                # print("-------------------", shipping_address, description, items_list)
            else:
                context = {
                    'form': form,
                    'formset': formset
                }
                return render(request, 'create_order.html', context)
            return render(request, "test.html", {'info': form.cleaned_data, 'info2': items_list})
    else:
        orders = Order.objects.all()
        context = {"orders": orders}
        return render(request, "order_list.html", context)


def order_detail(request, order_id):
    order_detail = Order.objects.get(pk=order_id)
    order_items = OrderItems.objects.filter(order__id=order_id).values('item_id', 'quantity', 'discount')
    for item in order_items:
        item['name'] = Item.objects.get(pk=item['item_id']).name
    print(order_detail, order_items)
    context = {
        "order_detail": model_to_dict(order_detail, fields=[field.name for field in order_detail._meta.fields]),
        "order_items": order_items
    }
    return render(request, "order_detail.html", context)


def test(request):
    return render(request, 'test.html')


# render the form
def order_create(request):
    print("----------testing---------------", request.POST)
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
                items_list.append((item, quantity))
            # print("-------------------", shipping_address, description, items_list)
            return render(request, "test.html", {'info': form.cleaned_data, 'info2': formset.cleaned_data})
    else:
        form = OrderForm(initial={'Shipping Address': "test string"})
        formset = ItemFormset()
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'create_order.html', context)


def test_order(request):
    print(request)
    pass
