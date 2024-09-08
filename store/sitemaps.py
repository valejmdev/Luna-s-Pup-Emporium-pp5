from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category  # Adjust imports as needed

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['store:index', 'store:all_products', 'store:special_offers', 
                'store:terms_conditions', 'store:privacy_policies', 
                'store:faq', 'store:about_us', 'store:contact_us']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Make sure Product model has an updated_at field

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()