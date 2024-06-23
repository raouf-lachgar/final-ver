# users/models.py
from django.db import models
#from algerography.models import Wilaya
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
class custom_user(AbstractUser):
    phone_num = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='user_pic/')
    def __str__(self):
        return self.username
class Wilaya(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
class Product(models.Model):
    user = models.ForeignKey("custom_user", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_serie = models.CharField(max_length=255)
    piece = models.CharField(max_length=255) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    STATE_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    state = models.CharField(max_length=4, choices=STATE_CHOICES)
    city = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    total_rating = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    @property
    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.total_rating / self.rating_count

    def __str__(self):
        return self.name
class car_model(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class car_serie(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class piece(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

    
class media_files(models.Model):
    product_id = models.ForeignKey("Product",on_delete=models.CASCADE)
    path = models.ImageField(upload_to='post_pic/')

User = get_user_model()

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    @classmethod
    def rate_product(cls, user, product, value):
        value = int(value)  # Ensure the value is an integer
        rating, created = cls.objects.get_or_create(user=user, product=product, defaults={'value': value})

        if not created:
            # If the rating already exists, subtract the old value from total_rating
            product.total_rating -= rating.value
            rating.value = value  # Update the value of the existing rating

        rating.save()
        # Add the new value to total_rating
        product.total_rating += value
        # Ensure rating_count is only incremented if the rating was newly created
        if created:
            product.rating_count += 1
        product.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=360)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.name}'
