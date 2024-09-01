from cart.views import get_or_create_cart
from .models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = get_or_create_cart(request.user)
            return {'cart_items_count': cart.items.count() if cart else 0}
        except Cart.DoesNotExist:
            return {'cart_items_count': 0}
    return {'cart_items_count': 0}


def cart_processor(request):
    cart = get_or_create_cart(request.user) if request.user.is_authenticated else None
    if cart is None:
        cart_items = []
    else:
        cart_items = CartItem.objects.filter(cart=cart)
    return {'cart_items': cart_items}