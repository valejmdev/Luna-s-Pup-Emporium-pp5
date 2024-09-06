from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured_image = CloudinaryField('image', default='placeholder')
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    on_sale = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_sale_price(self):
        if self.on_sale:
            discount = Decimal('0.75')  # Convert the float to a Decimal
            return round(self.price * discount, 2)  # Multiply Decimal by Decimal
        return self.price

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0.0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    featured_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return f"Image for {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    rating = models.PositiveIntegerField()  # Rating out of 5
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=100, choices=(
        ('General', 'General'),
        ('Product-Specific', 'Product-Specific'),
        ('Order and Shipping', 'Order and Shipping'),
        ('Returns and Exchanges', 'Returns and Exchanges'),
        ('Care and Maintenance', 'Care and Maintenance'),
    ))

    def __str__(self):
        return self.question
    
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email