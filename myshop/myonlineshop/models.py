from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm
from django.db.models import Avg, Count
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index = True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myonlineshop:product_list_by_category', args=[self.slug])

COLOR_CHOICES = (
    ('Red', 'R'),
    ('Black', 'B')
)

class Product(models.Model):
    
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    slider1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    slider2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    slider3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    variant =models.CharField(max_length=10,choices=VARIANTS, default='None')
    description = RichTextUploadingField()
    additional_information =  models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    Featured= models.BooleanField(default=False)
    Premium = models.BooleanField(default=False)
    New_arrivals = models.BooleanField(default=False)
    super_offer = models.BooleanField(default=False)
    super_offer2 = models.BooleanField(default=False)
    best = models.BooleanField(default=False)
    header_image = models.BooleanField(default=False)

    sale = models.BooleanField(default=False, verbose_name='pending payments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    size_cloth = models.BooleanField(default=True)
    size_trouser = models.BooleanField(default=True)
    

    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myonlineshop:product_detail', args=[self.id, self.slug])


    def avaregereview(self):
        reviews = Review.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Review.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/%Y/%m/%d', null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    user = models.ForeignKey(User,
                                on_delete=models.CASCADE, related_name='customer', null=True)
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='review', null=True)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    ip =  models.CharField(max_length=20, blank=True)
    rate = models.IntegerField(default=1)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Comment by {self.user} on {self.product}'

    def __str__(self):
        return f'Comment by user \n {self.comment}'

class CommentForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'comment', 'rate']



class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()



class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title


    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

class MailList(models.Model):
    email = models.EmailField()
    