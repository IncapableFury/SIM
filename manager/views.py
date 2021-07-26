from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.forms import formset_factory

from .models import Item, Order, OrderItems
from .forms import OrderForm, ItemFormset, UploadFileForm, ItemForm
from django.forms.models import model_to_dict
from django.db.models import Func, ProtectedError, Sum
from django.db import models, IntegrityError


# Create your views here.
# class view_inventory(ListView):
#     model = Item
#     context_object_name = "inventory"
#
#     def get_template_names(self):
#         return "item_list.html"


def view_inventory(request):
    inventory = Item.objects.all()
    cost_sum = Item.objects.aggregate(Sum('unit_price'))["unit_price__sum"]
    # template = loader.get_template('item_list.html')
    context = {
        'inventory': inventory,
        'cost_sum': cost_sum
    }
    return render(request, "item_list.html", context)


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
        # print("flags: ", request.POST['additems'], request.POST['removeitems'])
        # if request.POST['additems'] == 'true' or request.POST['removeitems'] == 'true':
        #     formset_dict_copy = request.POST.copy()
        #     if request.POST['additems'] == 'true':
        #         formset_dict_copy['form-TOTAL_FORMS'] = int(formset_dict_copy['form-TOTAL_FORMS']) + 1
        #         formset_dict_copy['additems'] = 'false'
        #     else:
        #         # print("we are good")
        #         formset_dict_copy['form-TOTAL_FORMS'] = int(formset_dict_copy['form-TOTAL_FORMS']) - 1
        #         formset_dict_copy['removeitems'] = 'false'
        #     # print("testing",formset_dict_copy)
        #     formset_initial = [{
        #         'quantity': 1, 'offset': 0.0, 'not_consume_inventory': False, 'item': '',
        #     } for _ in range(int(formset_dict_copy['form-TOTAL_FORMS']))]
        #     print(formset_dict_copy)
        #     formset = ItemFormset(formset_dict_copy
        #                           , initial=formset_initial
        #                           )
        #     # formset = ItemFormset.objects.create()
        #     form = OrderForm(request.POST, use_required_attribute=False)
        #     context = {
        #         'form': form,
        #         'formset': formset
        #     }
        #     return render(request, 'create_order.html', context)
        # else:  # create the real order
        print("are we even here?")
        form = OrderForm(request.POST)
        formset = ItemFormset(request.POST)
        items_list = []
        print("forms status: ", form.is_valid(), formset.is_valid(), form.errors, formset.errors,
              formset.non_form_errors())
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
                single_cost, single_profit = float(item.purchasing_price), float(item.unit_price) - float(
                    item.purchasing_price) - cost + float(
                    f.cleaned_data['offset'])
                cost += single_cost * f.cleaned_data["quantity"]
                profit += single_profit * f.cleaned_data["quantity"]
                # TODO: offset makes profit negative
                print(f.cleaned_data['not_consume_inventory'])
                if not f.cleaned_data['not_consume_inventory']:
                    try:
                        item.stock = item.stock - f.cleaned_data["quantity"]
                        item.save()
                    except IntegrityError:
                        f.add_error('quantity', ValidationError("Stock not enough"))
                        return render(request, 'create_order.html', {'form': form,
                                                                     'formset': formset})
            new_order = Order(shipping_address=shipping_address, description=description,
                              status=init_status, cost=cost, profit=profit, buyer=buyer,
                              tracking_number=tracking_number)
            new_order.save()
            for order_item_data in order_items_data:  # persist to db
                order_item = OrderItems(order=new_order, item=order_item_data['item_reference'],
                                        quantity=order_item_data['quantity'],
                                        offset=order_item_data['offset'])
                order_item.save()
                items_list.append(order_item_data)
            # print("-------------------", shipping_address, description, items_list)
        else:
            form.use_required_attribute = False
            print("testing error types:")
            for error in [form.errors, formset.errors, formset.non_form_errors]:
                print(type(error))
            errors = []
            for error in form.errors:
                print(form.errors[error])
                # errors.append(field + " : " + error)
            print(errors)
            context = {
                'form': form,
                'formset': formset,
                "errors": errors
            }
            return render(request, 'create_order.html', context)
        return redirect('/orders')
        # return render(request, "test.html", {'info': form.cleaned_data, 'info2': items_list})
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
        return redirect('manager/orders')
        # return render(request, "test.html", {'info': form.cleaned_data, 'info2': formset.cleaned_data})
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


def view_report(request):
    from django.db.models import Sum
    # TODO: query based on year; year default hard coded
    def num_format(x):
        return "{:.2f}".format(x) if x else 0.0

    year, month_str_representations = 2021, ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
                                             "Nov", "Dec"]
    order_month_entries = []
    order_year_entries = Order.objects.filter(created_time__year=year)
    year_profit, year_cost = 0, 0
    for month in range(1, 13):
        order_entries = order_year_entries.filter(created_time__month=month)
        month_profit = order_entries.aggregate(Sum('profit'))["profit__sum"]
        month_cost = order_entries.aggregate(Sum('cost'))["cost__sum"]
        year_profit += month_profit if month_profit else 0
        year_cost += month_cost if month_cost else 0
        order_month_entries.append((month_str_representations[month - 1],
                                    num_format(month_profit),
                                    num_format(month_cost),
                                    order_entries))
    context = {
        "orders": order_month_entries,
        "year_profit": num_format(year_profit),
        "year_cost": num_format(year_cost)
    }
    return render(request, 'view_reports.html', context)


def upload_excel(request):
    import pandas as pd
    import random
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            mode, file = form.cleaned_data["behavior"], request.FILES['file']
            redirect_to_inventory = True
            if mode == 'override':
                try:
                    Item.objects.filter(orderitems=None).delete()
                # TODO:handle error
                except ProtectedError:
                    redirect_to_inventory = False
                    form.add_error(None, "Can not flush database. Try append mode instead.")
            data = pd.read_excel(file)
            df = pd.DataFrame(data, columns=['name', 'stock', 'unit_price'])
            for idx, row in df.iterrows():
                name, stock, unit_price = row['name'], row['stock'], row['unit_price']
                purchasing_price = random.randint(1, unit_price)
                # print(row['name'], row['stock'], row['unit_price'])
                new_item = Item(name=name, stock=stock, unit_price=unit_price, purchasing_price=purchasing_price)
                new_item.save()
            if redirect_to_inventory:
                return redirect('/manager/inventory')
        else:
            pass
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'upload_excel.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')


def customers(request):
    return render(request, 'customer_list.html')
