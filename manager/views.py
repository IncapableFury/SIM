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
    if request.method == 'POST':  # TODO: add/remove item row; its logic shouldn't be there. no idea how
        print(request.POST)
        if request.POST['additems'] == 'true' or request.POST['removeitems'] == 'true':
            # print("we are good")
            formset_dict_copy = request.POST.copy()
            if request.POST['additems'] == 'true':
                formset_dict_copy['form-TOTAL_FORMS'] = int(formset_dict_copy['form-TOTAL_FORMS']) + 1
                formset_dict_copy['additems'] = 'false'
            else:
                # print("we are good")
                formset_dict_copy['form-TOTAL_FORMS'] = int(formset_dict_copy['form-TOTAL_FORMS']) - 1
                formset_dict_copy['removeitems'] = 'false'
            # print("testing",formset_dict_copy)
            formset = ItemFormset(formset_dict_copy)
            form = OrderForm(request.POST, use_required_attribute=False)
            context = {
                'form': form,
                'formset': formset
            }
            return render(request, 'create_order.html', context)
        else:  # create the real order
            print("are we even here?")
            form = OrderForm(request.POST)
            formset = ItemFormset(request.POST)
            items_list = []
            print(form.is_valid(), formset.is_valid(), formset.errors, formset.non_form_errors)
            # print(formset)
            if form.is_valid() and formset.is_valid():
                shipping_address = form.cleaned_data['shipping_address']
                description = form.cleaned_data['description']
                init_status = form.cleaned_data['status']
                buyer = form.cleaned_data['buyer']
                tracking_number = form.cleaned_data['tracking_number']
                cost = 0
                profit = 0
                order_items_data = []
                # print(formset)
                for f in formset:  # get data of each item, do validation here
                    item = Item.objects.get(name=f.cleaned_data["item"])
                    order_items_data.append({'item_reference': item, 'quantity': f.cleaned_data["quantity"],
                                             'offset': f.cleaned_data['offset']})
                    cost += float(item.purchasing_price)
                    profit += float(item.unit_price) - cost + float(f.cleaned_data['offset'])
                new_order = Order(shipping_address=shipping_address, description=description,
                                  status=init_status, cost=cost, profit=profit, buyer=buyer,
                                  tracking_number=tracking_number)
                new_order.save()
                for order_item_data in order_items_data:  # persist to db
                    order_item = OrderItems(order=new_order, item=order_item_data['item_reference'], quantity=order_item_data['quantity'],
                                            offset=order_item_data['offset'])
                    order_item.save()
                    items_list.append(order_item_data)

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
    order_items = OrderItems.objects.filter(order__id=order_id).values('item_id', 'quantity', 'offset')
    for item in order_items:
        item['name'] = Item.objects.get(pk=item['item_id']).name
    # print(order_detail, order_items)
    context = {
        "order_detail": model_to_dict(order_detail, fields=[field.name for field in order_detail._meta.fields]),
        "order_items": order_items
    }
    return render(request, "order_detail.html", context)


def test(request):
    return render(request, 'test.html')


# render the form
def order_create(request):
    # print("----------testing---------------", request.POST)
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
        form = OrderForm(use_required_attribute=False)
        formset = ItemFormset()
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'create_order.html', context)


def test_order(request):
    print(request)
    pass
