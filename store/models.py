from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
class CustomRequest(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, help_text="So we can contact you on WhatsApp")
    idea_description = models.TextField(help_text="Describe the colors, flowers, or theme you want.")
    reference_image = models.ImageField(upload_to='custom_requests/', blank=True, null=True, help_text="Upload a screenshot or photo of what you want.")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.name}"