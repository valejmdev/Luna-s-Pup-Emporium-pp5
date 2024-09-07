from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, FAQ
from django.db.models import Q, Avg
from checkout.models import Order
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import NewsletterForm
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm


def product_list(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()
    else:
        products = Product.objects.all()

    search_term = request.GET.get('q', '')

    # Apply search filter
    if search_term:
        products = products.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )

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

    # Handle review form submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('store:product_detail', product_id=product.id)
        else:
            messages.error(request, "There was an issue with your review submission.")
    else:
        form = ReviewForm()

    # Fetch existing reviews
    reviews = product.reviews.all()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images,
        'form': form,
        'reviews': reviews
    })

# View to display all products
def all_products(request):
    """A view to show all products, including sorting and searching queries"""

    search_term = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')

    products = Product.objects.all()

    # Apply search filter
    if search_term:
        products = products.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )

    # Sorting
    if sort_by == 'price':
        if sort_order == 'desc':
            products = products.order_by('-price')
        else:
            products = products.order_by('price')
    elif sort_by == 'rating':
        if sort_order == 'desc':
            products = products.order_by('-avg_rating')
        else:
            products = products.order_by('avg_rating')
    else:
        if sort_order == 'desc':
            products = products.order_by('-name')
        else:
            products = products.order_by('name')

    # Calculate sale price and average rating
    for product in products:
        product.sale_price = product.get_sale_price()
        product.avg_rating = product.average_rating()

    context = {
        'products': products,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'search_term': search_term
    }

    return render(request, 'store/all_products.html', context)

def special_offers(request):
    products_on_sale = Product.objects.filter(on_sale=True)
    for product in products_on_sale:
        product.sale_price = product.get_sale_price()
    return render(request, 'store/special_offers.html', {'products': products_on_sale})

def index(request):
    featured_products = Product.objects.filter(featured=True)  # Fetch featured products
    for product in featured_products:
        product.sale_price = product.get_sale_price()
        product.avg_rating = product.average_rating()
    
    return render(request, 'store/index.html', {'featured_products': featured_products})

def faq(request):
    faqs = FAQ.objects.all().order_by('category')
    return render(request, 'store/faq.html', {'faqs': faqs})

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

def terms_conditions(request):
    return render(request, 'store/terms_conditions.html')

def privacy_policies(request):
    return render(request, 'store/privacy_policies.html')

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # Save the subscription
            subscriber = form.save()

            # Send confirmation email
            subject = "Thank you for subscribing to Luna’s Pup Emporium!"
            message = "You've successfully subscribed to our newsletter."
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [subscriber.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, "Subscription successful! A confirmation email has been sent.")
            except Exception as e:
                messages.error(request, "There was an issue sending the confirmation email.")
            
            # Redirect to a confirmation page or render the same page
            return render(request, 'store/newsletter_confirmation.html')
        else:
            messages.error(request, "There was an error with your subscription.")
    else:
        form = NewsletterForm()

    return render(request, 'store/newsletter.html', {'form': form})

def article_detail(request, slug):
    articles = {
        'summer-safety-tips': {
            'title': "Summer Safety Tips for Your Dog",
            'introduction': "As the temperature rises, it's important to keep our furry friends safe and comfortable. Dogs can easily overheat in hot weather, which can lead to serious health issues. In this article, we share essential tips to ensure your dog stays cool, hydrated, and happy during the summer months.",
            'content': [
                "Provide Plenty of Water: Always make sure your dog has access to fresh, clean water. Consider adding ice cubes to their water bowl to keep it cool for longer periods.",
                "Limit Exercise During Peak Hours: Avoid walking your dog during the hottest parts of the day, typically between 10 AM and 4 PM. Early morning or late evening walks are safer.",
                "Use Sunscreen for Sensitive Areas: Dogs can get sunburned too! Apply pet-safe sunscreen to their nose, ears, and belly if they have thin fur or light skin.",
                "Never Leave Your Dog in a Hot Car: Even with the windows cracked, the temperature inside a car can rise dangerously fast. Always take your dog with you or leave them at home where it's cool.",
                "Provide Shade and Cooling Pads: If your dog spends time outside, ensure they have access to shaded areas. You can also use cooling pads or a kiddie pool filled with cool water for them to lie in.",
                "Watch for Signs of Heatstroke: Symptoms include excessive panting, drooling, lethargy, and vomiting. If you suspect your dog is overheating, move them to a cooler place, offer water, and contact your vet immediately.",
            ],
            'conclusion': "By following these summer safety tips, you can ensure that your dog enjoys the sunny season without any risks. Keep an eye on them, and prioritize their comfort during the hot days ahead."
        },
        'top-dog-toys-2024': {
            'title': "Top 10 Dog Toys of 2024",
            'introduction': "Keeping your dog entertained and mentally stimulated is key to their happiness and well-being. With so many toys on the market, it can be overwhelming to choose the right ones. That's why we've compiled a list of the top 10 dog toys of 2024, featuring options that are fun, durable, and loved by dogs of all sizes.",
            'content': [
                "The Indestructi-Ball: Perfect for heavy chewers, this durable ball withstands even the toughest jaws. It's great for fetch and can be used indoors or outdoors.",
                "Puzzle Feeder Toy: This interactive toy challenges your dog to work for their food, providing mental stimulation and slowing down fast eaters.",
                "Squeaky Plush Toy: A favorite among small dogs, this plush toy comes in various shapes and characters, offering endless squeaky fun.",
                "Rope Tug Toy: Great for interactive play, this sturdy rope toy is ideal for games of tug-of-war and helps keep your dog's teeth clean.",
                "Automatic Ball Launcher: Perfect for energetic dogs, this device launches balls for your dog to fetch, providing hours of fun and exercise.",
                "Treat-Dispensing Toy: This toy releases treats as your dog plays with it, making it a great option for keeping them entertained while rewarding good behavior.",
                "Flying Disc: Lightweight and durable, this flying disc is perfect for games of fetch at the park. It's easy to throw and floats in water, making it ideal for summer play.",
                "Interactive Laser Toy: Ideal for indoor play, this laser toy moves randomly across the floor, encouraging your dog to chase and pounce.",
                "Stuffed Kong Toy: Fill this durable rubber toy with peanut butter or treats, and watch your dog stay entertained as they try to get to the goodies inside.",
                "Snuffle Mat: This innovative mat hides treats among its fabric folds, challenging your dog to use their sense of smell to find them.",
            ],
            'conclusion': "These top 10 dog toys of 2024 offer something for every dog, from chewers to fetch lovers. By incorporating a variety of toys into your dog's routine, you can keep them engaged, happy, and healthy all year long."
        },
        'eco-friendly-dog-beds': {
            'title': "Introducing Our New Eco-Friendly Dog Beds",
            'introduction': "At Luna's Pup Emporium, we're committed to offering products that are not only comfortable for your dog but also kind to the planet. That's why we're excited to introduce our new line of eco-friendly dog beds, made from sustainable materials that benefit both your pet and the environment.",
            'content': [
                "Sustainable Materials: Our eco-friendly dog beds are made from recycled plastic bottles, organic cotton, and natural latex. These materials are carefully selected to provide comfort and durability while reducing environmental impact.",
                "Stylish Designs: Just because something is eco-friendly doesn't mean it can't be stylish! Our dog beds come in a variety of colors and patterns, ensuring they look great in any home.",
                "Hypoallergenic and Safe: The materials used in our beds are hypoallergenic, making them ideal for dogs with sensitive skin or allergies. They're also free from harmful chemicals and dyes.",
                "Easy to Clean: Each bed features a removable, machine-washable cover, so you can keep it fresh and clean with minimal effort.",
                "Long-Lasting Comfort: Designed to provide optimal support, our beds are perfect for dogs of all sizes and ages, including those with joint issues or arthritis. The natural latex filling conforms to your dog's shape, offering superior comfort.",
                "Environmentally Conscious: By choosing our eco-friendly dog beds, you're not just giving your dog a cozy place to sleep—you're also making a positive impact on the environment. For every bed sold, we donate a portion of the proceeds to environmental conservation efforts.",
            ],
            'conclusion': "Our new eco-friendly dog beds are the perfect choice for conscientious pet owners who want to provide their dogs with the best while also caring for the planet. Explore our collection today and find the perfect bed for your furry friend."
        },
    }

    # Retrieve the correct article based on the slug
    article = articles.get(slug)

    # If the article is not found, you can handle the error (e.g., 404 page)
    if not article:
        return render(request, 'store/404.html')

    return render(request, 'store/article_detail.html', {'article': article})

@login_required
def order_detail(request, order_id):
    # Fetch the order object
    order = get_object_or_404(Order, id=order_id)

    # Check if the order belongs to the currently logged-in user
    if order.user != request.user:
        # If not, redirect to an error page or a different view
        messages.error(request, "You do not have permission to view this order.")

        # Fetch featured products for the index view
        featured_products = Product.objects.filter(featured=True)
        for product in featured_products:
            product.sale_price = product.get_sale_price()
            product.avg_rating = product.average_rating()

        return render(request, 'store/index.html', {'featured_products': featured_products})

    # If the user owns the order, render the order detail page
    return render(request, 'store/order_detail.html', {'order': order})

def send_order_confirmation(request, order_id):
    # Fetch order details and customer email
    customer_email = 'customer@example.com'
    subject = 'Order Confirmation'
    body = 'Thank you for your order!'

    send_mail(customer_email, subject, body)

    return render(request, 'store/confirmation.html')