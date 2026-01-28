from .cart import Cart

def cart_count(request):
    # This makes the variable 'cart' available on every single page
    return {'cart': Cart(request)}