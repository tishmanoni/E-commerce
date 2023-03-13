from django.contrib import admin
from .models import Category, Product, Review, Color, Size, Variants, MailList, Images
import admin_thumbnails
from myonlineshop.models import models

# Register your models here.

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    extra = 1
    show_change_link = True

@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image','price','quantity', 'variant', 'available', 'created', 'updated', 'best', 'sale', 'Featured', 'New_arrivals', 'Premium', 'super_offer', 'super_offer2']
    inlines = [
        ProductVariantsInline ,ProductImageInline
    ]

    # list_filter = ['available', 'created', 'updated']
    
    list_editable = ['price', 'quantity', 'variant', 'available', 'sale', 'best','Featured', 'New_arrivals', 'Premium',]
    prepopulated_fields = {'slug': ('name',)}
    



    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ( 'subject','comment', 'user', 'product', 'created', 'active', 'status')
    # list_filter = ('active', 'created', 'updated')
    # search_fields = ('name', 'email', 'body')
    list_editable = ("status",)
    

@admin.register(MailList)
class MailAdmin(admin.ModelAdmin):
    list_display = ('email',)


    

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']



@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']

admin.site.register(Variants,VariantsAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)