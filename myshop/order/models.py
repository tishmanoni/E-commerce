from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.db import models
from myonlineshop.models import Product
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from coupons.models import Coupon

from django.conf import settings
from django.utils.translation import gettext_lazy as _
   
    
class Order(models.Model):

    state_choice = (
        ('Abia', 'Abia'),
        ('Adamawa', 'Adamawa'),
        ('Akwa Ibom', 'Akwa Ibom'),
        ('Anambra', 'Anambra'),
        ('Bauchi', 'Bauchi'),
        ('Bayelsa', 'Bayelsa'),
        ('Benue', 'Benue'),
        ('Borno', 'Borno'),
        ('Cross River', 'Cross River'),
        ('Delta', 'Delta'),
        ('Ebonyi', 'Ebonyi'),
        ('Edo', 'Edo'),
        ('Ekiti', 'Ekiti'),
        ('Enugu', 'Enugu'),
        ('Gombe', 'Gombe'),
        ('Imo', 'Imo'),
        ('Jigawa', 'Jigawa'),
        ('Kaduna', 'Kaduna'),
        ('Kano', 'Kano'),
        ('Katsina', 'Katsina'),
        ('Kebbi', 'Kebbi'),
        ('Kogi', 'Kogi'),
        ('Kwara', 'Kwara'),
        ('Lagos', 'Lagos'),
        ('Nasarawa', 'Nasarawa'),
        ('Niger', 'Niger'),
        ('Ogun', 'Ogun'),
        ('Ondo', 'Ondo'),
        ('Osun', 'Osun'),
        ('Oyo', 'Oyo'),
        ('Plateau', 'Plateau'),
        ('Rivers', 'Rivers'),
        ('Sokoto', 'Sokoto'),
        ('Taraba', 'Taraba'),
        ('Yobe', 'Yobe'),
        ('Zamfara','Zamfara')
    )

    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('Postal code'),max_length=20)
    city = models.CharField(_('city'),max_length=100)
    state = models.CharField(choices=state_choice, default='Lagos', max_length=200 )
    country = CountryField(blank_label='(select country)')
    phone_number = models.CharField(max_length=14)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                  validators=[MinValueValidator(0),
                                      MaxValueValidator(100)])
    # shipping = models.DecimalField(default=1000, decimal_places=2, )
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * \
            (self.discount / Decimal(100))
    def get_total_cost_shipping(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100)) + Decimal(1200)
    

    # def get_absolute_url(self):
    #     return reverse('orders:my_order',args=[self.id,
    #                             self.user_id,
    #                             ])
class OrderItem(models.Model):
    Size_choice = (
        
        ("None","None"),
        ('S', 'Small'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ("39", "39"),
        ("40", "40"),
        ("41", "41"),
        ("42", "42")
        
         )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size_cloth =models.CharField(max_length=200, choices=Size_choice, default='None')

    class Meta:
        unique_together = ('user', 'order', 'product', 'price', 'quantity')
    def __str__(self):
        return str(self.user)
    def get_cost(self):
        return self.price * self.quantity

    def get_absolute_url(self):
        return reverse('orders:order_item',args=[self.product_id, self.quantity, self.order_id,
                                self.user_id
                                ])

