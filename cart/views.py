from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.http import JsonResponse
from .models import Cart, CartItem
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CartItemForm


def get_or_create_cart(user):
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    else:
        return None


@login_required
def cart_add(request, product_id):
    cart = get_or_create_cart(request.user)
    product = get_object_or_404(Product, id=product_id)

    form = CartItemForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        if quantity < 1 or quantity > 10:
            messages.error(request, 'Quantity must be between 1 and 10.')
        else:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, 'Item added to cart.')
    else:
        messages.error(request, 'Invalid quantity.')

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = get_or_create_cart(request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
            'cart_items': cart_items, 'total_price': total_price})


@login_required
@require_POST
def update_cart(request):
    cart = get_or_create_cart(request.user)
    if not cart:
        return JsonResponse({'error': 'Cart not found'}, status=400)

    updated_items = {}
    errors = {}
    
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            product_id = key.replace('quantity_', '')
            form = CartItemForm({'quantity': value})
            if form.is_valid():
                quantity = form.cleaned_data.get('quantity')
                product = get_object_or_404(Product, id=product_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cart_item.quantity = quantity
                cart_item.save()
                updated_items[product_id] = quantity
            else:
                errors[product_id] = [{'message': error} for error in form.errors.get('quantity', [])]

    # Calculate updated total price
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price for item in cart_items)

    response_data = {
        'total_price': total_price,
        'updated_items': updated_items,
        'errors': errors
    }

    return JsonResponse(response_data)
