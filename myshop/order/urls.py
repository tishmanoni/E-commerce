from django.urls import path
from . import views
# from paystack.views import delete_order
app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    # path('myorder/<int:id>/<int:user_id>/', views.my_order, name='my_order'),
    path('allorders/', views.all_orders, name='all_order'),
    path('orderitem/<int:product_id>/<int:quantity>/<int:order_id>/<int:user_id>/', views.my_order, name='order_item'),
    path('admin/order/<int:order_id>/<int:user_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf, name='admin_order_pdf'),
    path('delete/<int:id>/', views.delete, name='delete-person'),
    # path('deleteorder/<int:id>', views.delete_order, name='user_deleteorder'),
]
