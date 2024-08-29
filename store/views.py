from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q, Avg

def product_list(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()
    else:
        products = Product.objects.all()

    for product in products:
        product.sale_price = product.get_sale_price()  # Calculate sale price
        product.avg_rating = product.average_rating()

    return render(request, 'store/product_list.html', {'products': products, 'category_slug': category_slug})

# Product Detail View: Displays details of a single product
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()  # Fetching related product images

    # Sale price and rating
    product.sale_price = product.get_sale_price()
    product.avg_rating = product.average_rating()

    return render(request, 'store/product_detail.html', {'product': product, 'images': images})

# View to display all products
def all_products(request):
    """A view to show all products, including sorting and search queries"""
    
    query = request.GET.get('q')  # Get the query from the search bar
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'store/all_products.html', context)

def special_offers(request):
    products_on_sale = Product.objects.filter(on_sale=True)
    for product in products_on_sale:
        product.sale_price = product.get_sale_price()
    return render(request, 'store/special_offers.html', {'products': products_on_sale})

def index(request):
    return render(request, 'store/index.html')

def faq(request):
    return render(request, 'store/faq.html')

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

def terms_conditions(request):
    return render(request, 'store/terms_conditions.html')

def newsletter(request):
    # Your view logic here
    return render(request, 'store/newsletter.html')

