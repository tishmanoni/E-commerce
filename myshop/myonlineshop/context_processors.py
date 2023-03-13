from .views import product_list
def category(request):
    return{'categories':product_list(request)}