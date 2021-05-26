from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .models import Item
from .forms import OrderForm

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
        form = OrderForm(request.POST)
        if form.is_valid():
            shipping_address = form.cleaned_data['shipping_address']
            description = form.cleaned_data['description']
            print("-------------------", form, shipping_address, description)
            return render(request, "test.html", {'info':form.cleaned_data})
    return render(request, "test.html", {'info':"Viewing all orders"})

def test(request):
    return render(request, 'test.html')

# render the form
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            shipping_address = form.cleaned_data['shipping_address']
            description = form.cleaned_data['description']
            print("-------------------", form, shipping_address, description)
            return render(request, "test.html", {'info':form.cleaned_data})
    else:
        form = OrderForm(initial={'address':"test string"})
    context={
        'form': form
    }
    return render(request, 'create_order.html', context)

def test_order(request):
    print(request)
    pass
