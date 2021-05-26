from django.urls import path

from . import views

app_name = 'manager'
urlpatterns = [
    path('inventory', views.view_inventory.as_view(), name='view_inventory'),
    path('item/<int:pk>', views.view_item_detail.as_view(), name='view_item_detail'),
    path('order-create', views.order_create, name='create_order'),
    path('test_order', views.orders, name='orders'),
    path('orders', views.orders, name='orders'),
    path('test', views.test,name='test')
]