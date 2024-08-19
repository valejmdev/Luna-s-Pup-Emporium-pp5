from django.shortcuts import render

def checkout(request):
    return render(request, 'checkout/checkout.html')

def order_confirmation(request):
    return render(request, 'checkout/order_confirmation.html')