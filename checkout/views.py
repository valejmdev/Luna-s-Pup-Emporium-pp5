from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, OrderLineItem
from cart.models import Cart, CartItem
from profiles.models import UserProfile 

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to proceed to checkout.")
        return redirect('login')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            
            try:
                cart = Cart.objects.get(user=request.user)
                cart_items = CartItem.objects.filter(cart=cart)
            except Cart.DoesNotExist:
                cart_items = []

            # Link the order to the logged-in user
            order.user = request.user  # This ensures the order is tied to the logged-in user

            order.save()

            for item in cart_items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    lineitem_total=item.total_price,
                )
            
            order.update_total()

            stripe_total = int(order.grand_total * 100)

            if stripe_total < 50:
                messages.error(request, "The order total is too small for payment.")
                return redirect('checkout')

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
            messages.error(request, "There was an error with your form.")
    else:
        order_form = OrderForm()

        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_items = []

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

        # Send order confirmation email if needed
        # send_order_confirmation_email(order)

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

@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Ensure only the authenticated user who placed the order can view it
    if request.user.is_authenticated:
        if order.user != request.user:
            messages.error(request, "You are not authorized to view this order.")
            return redirect('store:index')

    # Proceed with rendering the order confirmation
    context = {
        'order': order,
    }

    return render(request, 'checkout/order_confirmation.html', context)
