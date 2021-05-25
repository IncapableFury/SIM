from django.urls import path

from . import views

app_name = 'manager'
urlpatterns = [
    path('inventory', views.view_inventory.as_view(), name='view_inventory'),
    path('item/<int:pk>', views.view_item_detail.as_view(), name='view_item_detail'),
    path('orders', views.view_orders, name='view_orders'),
    path('test', views.test,name='test')
]