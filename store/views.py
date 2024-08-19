from django.shortcuts import render

def index(request):
    return render(request, 'store/index.html')

def product_list(request):
    return render(request, 'store/product_list.html')

def product_list_by_category(request, category_slug):
    return render(request, 'store/product_list_by_category.html')

def product_detail(request, slug):
    return render(request, 'store/product_detail.html')

def faq(request):
    return render(request, 'store/faq.html')

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')