from django.contrib import admin
from .models import Product, Category, ProductImage, Review, FAQ, NewsletterSubscriber


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
         'name', 'price', 'on_sale', 'rating', 'get_sale_price', 'featured')
    list_filter = ('on_sale', 'featured')
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'featured_image')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment')


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    search_fields = ('question', 'answer')
    list_filter = ('category',)


admin.site.register(FAQ, FAQAdmin)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_on')
    search_fields = ('email',)