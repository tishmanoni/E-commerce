from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from myonlineshop.models  import Product, Category
from django.contrib import messages
from django.urls import reverse
# import weasyprint
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
# from celery import task
# import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from order.models import Order




def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.user.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'info@tishman.com.ng',
                          [order.user.email])
    return mail_sent


def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'info@tishman.com.ng',
                         [order.user.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    # stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    # weasyprint.HTML(string=html).write_pdf(out,
    #                                       stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()

@login_required
def order_create(request):
    cart = Cart(request)
    my_product = Product()

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)



        if form.is_valid():
            data = Order() #create relation to model
            data.address = form.cleaned_data['address']
            data.postal_code = form.cleaned_data['postal_code']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.phone_number = form.cleaned_data['phone_number']
            current_user = request.user
            data.user_id = current_user.id
            order = data
            # order = form.save(commit=False)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.save()


            for item in cart:
                OrderItem.objects.create(user=request.user,
                                            order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity'],
                                            size_cloth= item["size_cloth"]
                                            )

            # launch asynchronous task
            #order_created(order.id)
            # return render(request, 'orders/order/created.html', locals())
            #set the order in the session
            request.session['order_id'] = order.id
            # clear the cart
            cart.clear()
            # redirect for payment
            return redirect(reverse('paystack:payment'))
        else:
            order_created(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})

    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})



@staff_member_required
def admin_order_detail(request, order_id, user_id):
    order = get_object_or_404(Order, id=order_id, user_id=user_id)
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})



@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


@login_required
def my_order(request, product_id, quantity, order_id, user_id):
    # myorder = get_object_or_404(Order, id=id, user_id=user_id )
    order_detail = get_object_or_404(OrderItem, product=product_id, quantity=quantity ,order_id=order_id,  user_id=request.user)
    orders = Order.objects.all()
    order_item = OrderItem.objects.filter(user=user_id)
    categories = Category.objects.all()

    return render(request, 'orders/order/myorders.html', {'orders':orders, 'order_detail':order_detail, 'order_item':order_item, 'categories':categories} )

@login_required
def all_orders(request):
    orders = OrderItem.objects.order_by('order')
    orders_filter = orders.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'orders/order/allorders.html', {'orders':orders, 'filter':orders_filter, 'categories':categories} )


@login_required
def delete(request, id):
    # person_pk = request.session.get('order_id')
    current_user = request.user
    Order.objects.filter(id=id, user_id=current_user.id).delete()
    # query = Order.objects.get(id=person_pk)
    # query.delete()
    messages.success(request, 'Order canceled')
    return HttpResponseRedirect('/orders/allorders')

# @login_required(login_url='/login') # Check login
# def user_deletecomment(request,id):
#     current_user = request.user
#     Comment.objects.filter(id=id, user_id=current_user.id).delete()
#     messages.success(request, 'Comment deleted..')
#     return HttpResponseRedirect('/user/comments')