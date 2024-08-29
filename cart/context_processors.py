from cart.views import get_or_create_cart
from .models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        return {'cart_items_count': cart.items.count()}
    return {'cart_items_count': 0}


def cart_processor(request):
    cart = get_or_create_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return {'cart_items': cart_items}