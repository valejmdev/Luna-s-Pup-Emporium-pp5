from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging

from .forms import OrderForm
from .models import Order, OrderLineItem
from cart.models import Cart, CartItem

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to proceed to checkout.")
        return redirect('login')  # or whatever your login URL is

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Create order instance but don't save it yet
            order = order_form.save(commit=False)
            
            # Retrieve the user's cart
            try:
                cart = Cart.objects.get(user=request.user)
                cart_items = CartItem.objects.filter(cart=cart)
            except Cart.DoesNotExist:
                cart_items = []

            # Save the order instance
            order.save()

            # Create order line items
            for item in cart_items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    lineitem_total=item.total_price,
                )
            
            # Update the order totals
            order.update_total()

            # Calculate the total amount in cents for Stripe
            stripe_total = int(order.grand_total * 100)
            logger.debug(f'Order grand total (cents): {stripe_total}')

            MINIMUM_AMOUNT_CENTS = 50
            if stripe_total < MINIMUM_AMOUNT_CENTS:
                messages.error(request, f"The order total is too small for payment. Minimum amount is {MINIMUM_AMOUNT_CENTS / 100} USD.")
                return redirect('checkout')

            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                metadata={'order_id': order.order_number},
            )

            context = {
                'order': order,
                'order_form': order_form,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'client_secret': intent.client_secret,
            }

            return render(request, 'checkout/payment.html', context)
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
    else:
        order_form = OrderForm()

        # Retrieve the user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_items = []

        # Calculate the total price from cart items
        total = sum(item.total_price for item in cart_items)

        context = {
            'order_form': order_form,
            'cart_items': cart_items,
            'total': total,
        }

    return render(request, 'checkout/checkout.html', context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)

    return HttpResponse(status=200)


def handle_successful_payment(payment_intent):
    """
    Update the order status when the payment is successful.
    Use the order_id stored in the Stripe metadata to locate the order.
    """
    order_id = payment_intent['metadata']['order_id']
    try:
        order = Order.objects.get(order_number=order_id)
        order.status = 'Paid'
        order.save()

        return redirect('order_confirmation', order_number=order_id)

    except Order.DoesNotExist:
        pass


def handle_failed_payment(payment_intent):
    order_id = payment_intent['metadata']['order_id']
    try:
        order = Order.objects.get(order_number=order_id)
        order.status = 'Payment Failed'
        order.save()
    except Order.DoesNotExist:
        pass


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.user.is_authenticated and order.user != request.user:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('home') 
    
    context = {
        'order': order,
    }
    
    return render(request, 'checkout/order_confirmation.html', context)