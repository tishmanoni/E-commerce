from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from order.models import OrderItem, Order
from myonlineshop.models import Product, Category, Review
from cart.cart import Cart
from cart.views import cart_detail
from myonlineshop.models import Category, Product, Review
# from myonlineshop.forms import ReviewForm





# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated '\
#                                         'successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    # messages.success(request, 'Succesfully Logged in')
    current_user = request.user  # Access User Session information
    # profile = Profile.objects.get(user_id=current_user.id)
    categories = Category.objects.all()
    cart = Cart(request)
    if cart:
        return redirect('cart:cart_detail')
    else:
        return render(request,'account/dashboard.html',{'section': 'dashboard', 'categories':categories})



def register(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user, 'categories':categories})
    else:
        user_form = UserRegistrationForm()
        categories = Category.objects.all()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form, 'categories':categories})

from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.warning(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})



def user_comments(request):
    #category = Category.objects.all()
    current_user = request.user
    comments = Review.objects.filter(user_id=current_user.id)
    context = {
        #'category': category,
        'comments': comments,
    }
    return render(request, 'user_comment.html', context)


