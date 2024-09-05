from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.http import JsonResponse
from .models import Cart, CartItem
from django.views.decorators.http import require_POST


def get_or_create_cart(user):
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    else:
        return None

def cart_add(request, product_id):
    cart = get_or_create_cart(request.user)
    product = get_object_or_404(Product, id=product_id)

    quantity = request.POST.get('quantity', '1')
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')
    except (ValueError, ValidationError) as e:
        messages.error(request, f'Invalid quantity: {e}')
        return redirect('store:product_detail', product_id=product_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = get_or_create_cart(request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = get_or_create_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@require_POST
def update_cart(request):
    cart = get_or_create_cart(request.user)  # Get or create cart for authenticated user
    if not cart:
        return JsonResponse({'error': 'Cart not found'}, status=400)

    updated_items = {}
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            product_id = key.replace('quantity_', '')
            try:
                quantity = int(value)
                if quantity <= 0:
                    raise ValidationError('Quantity must be greater than zero.')
                
                product = get_object_or_404(Product, id=product_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity = quantity
                
                cart_item.save()
                updated_items[product_id] = quantity
            except (ValueError, ValidationError) as e:
                return JsonResponse({'error': str(e)}, status=400)

    # Calculate updated total price
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price for item in cart_items)
    
    response_data = {
        'total_price': total_price,
        'updated_items': updated_items
    }
    
    return JsonResponse(response_data)
