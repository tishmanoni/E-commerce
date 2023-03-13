from django.urls import reverse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from order.models import OrderItem, Order
from decimal import Decimal

# Create your views here.

def my_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost() + Decimal(20)

    # if request.method == 'POST':
    #     order.paid=True
    #     order.save()
    #     return redirect('payment:done')
    # else:
    return render(request, 'payment/pay.html', {'total_cost':total_cost})

def payment_done(request):
    return render(request, 'payment/done.html')
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


# def payment_process(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#     total_cost = order.get_total_cost()
#     if request.method == 'POST':