from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Product List View: Displays all products in a specific category
def product_list(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()  # Using related_name='products'
    else:
        products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products, 'category_slug': category_slug})

# Product Detail View: Displays details of a single product
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()  # Fetching related product images
    return render(request, 'products/product_detail.html', {'product': product, 'images': images})

# View to display all products
def all_products(request):
    products = Product.objects.all()
    return render(request, 'store/all_products.html', {'products': products})

def index(request):
    return render(request, 'store/index.html')

def faq(request):
    return render(request, 'store/faq.html')

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')