from django.contrib.auth.models import User
from django.db import models
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.utils.translation import gettext as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    


class Ingredients(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Categoria(models.Model):
    categoria = models.CharField(max_length=255)
    
    def __str__(self):
        return self.categoria

class FoodProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/food_products/', default="static/food_products/default")
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredients, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE)

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('pix', 'PIX'),
        ('credit_card', 'Credit Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.CharField(max_length=1000)
    order_datetime = models.DateTimeField()
    pickup_time = models.DateTimeField()
    total = models.DecimalField(max_digits=6, decimal_places=2)
    obs = models.TextField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True)
    order_status = models.CharField(max_length=20, blank=True) #active/ canceled/ finished


    
class CreditCard(models.Model):
    name = models.CharField(max_length=60)
    card_number = CardNumberField(_('card number'))
    expiry_date = CardExpiryField(_('expiration date'))
    cvv_code = SecurityCodeField(_('security code'))

class CartObs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_box_obs = models.TextField(blank=True)
