from django.urls import path

from . import views

app_name = 'manager'
urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('inventory', views.view_inventory, name='view_inventory'),
    path('customers', views.customers,name='customers'),
    path('item/<int:pk>', views.view_item_detail.as_view(), name='view_item_detail'),
    path('order-create', views.order_create, name='create_order'),
    path('test_order', views.orders, name='orders'),
    path('orders', views.orders, name='orders'),
    path('orders/<int:order_id>', views.order_detail, name="order_detail"),
    path('reports', views.view_report, name="view_reports"),
    path('test', views.test,name='test'),
    path('inventory/upload', views.upload_excel, name='upload_excel')
]