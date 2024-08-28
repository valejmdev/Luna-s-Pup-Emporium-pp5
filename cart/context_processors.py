from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        return {'cart_items_count': cart.items.count()}
    return {'cart_items_count': 0}