
import json
import base64
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import RedirectView, TemplateView
# Create your views here.
from . import settings, signals, utils
from .signals import payment_verified
from .utils import load_lib
from django.contrib import messages
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from order.models import OrderItem, Order
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from order.views import payment_completed


def payment(request):
    order_id = request.session.get('order_id')
    
    
    # order_detail = get_object_or_404(OrderItem ,order_id=order_id,  user_id=request.user )

    
    orders = OrderItem.objects.all()
    orders_filter = orders.filter(user=request.user, order_id=order_id)
    order = get_object_or_404(Order, id=order_id)
    total_cost_before_shipping = order.get_total_cost()
    total_cost = order.get_total_cost() + Decimal(1200)
    # del_order = Order.objects.filter(id=order_id).delete()
    

    # if request.method == 'POST':
    #     order.paid=True
    #     order.save()
    #     return redirect('payment:done')
    # else:
    # return render(request, 'payment/pay.html', )
    return render(request, 'paystack/sample.html', {'total_cost':total_cost, 'filter':orders_filter, 'order_id':order_id, 'total_cost_before_shipping':total_cost_before_shipping})

def delete(request, id):
    person_pk = request.session.get('order_id')
    current_user = request.user
    Order.objects.filter(id=person_pk, user_id=current_user.id).delete()
    # query = Order.objects.get(id=person_pk)
    # query.delete()
    messages.success(request, 'Order deleted, Continue Shopping')
    return HttpResponseRedirect('/store')

def all_orders(request):
    orders = OrderItem.objects.order_by('order')
    orders_filter = orders.filter(user=request.user)
    return render(request, 'paystack/sample.html', {'filter':orders_filter})

def success(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    payment_completed(order.id)
    return render(request, 'paystack/success-page.html', {'order':order})

def verify_payment(request, order):
    amount = request.GET.get('amount')
    txrf = request.GET.get('trxref')
    PaystackAPI = load_lib()
    paystack_instance = PaystackAPI()
    response = paystack_instance.verify_payment(txrf, amount=int(amount))
    if response[0]:
        payment_verified.send(
            sender=PaystackAPI,
            ref=txrf, amount=int(amount) / 100, order=order)
    return redirect(reverse('paystack:successful_verification', args=[order]))
    # return redirect(reverse('paystack:failed_verification', args=[order]))


class FailedView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_FAILED_URL == 'paystack:failed_page':
            return reverse(settings.PAYSTACK_FAILED_URL)
        return settings.PAYSTACK_FAILED_URL


def success_redirect_view(request, order_id):
    url = settings.PAYSTACK_SUCCESS_URL
    if url == 'paystack:success_page':
        url = reverse(url)
    return redirect(url, permanent=True)

def failure_redirect_view(request, order_id):
    url = settings.PAYSTACK_FAILED_URL
    if url == 'paystack:failed_page':
        url = reverse(url)
    return redirect(url, permanent=True)

class SuccessView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        if settings.PAYSTACK_SUCCESS_URL == 'paystack:success_page':
            return reverse(settings.PAYSTACK_SUCCESS_URL)
        return settings.PAYSTACK_SUCCESS_URL


def webhook_view(request):
    # ensure that all parameters are in the bytes representation
    digest = utils.generate_digest(request.body)
    signature = request.META['HTTP_X_PAYSTACK_SIGNATURE']
    if digest == signature:
        payload = json.loads(request.body)
        signals.event_signal.send(
            sender=request, event=payload['event'], data=payload['data'])
    return JsonResponse({'status': "Success"})
