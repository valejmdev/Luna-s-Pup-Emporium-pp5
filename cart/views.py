from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem

def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

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