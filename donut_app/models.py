from django.db import models
from django.urls import reverse

class Donut(models.Model):
    DONUT_LABEL_CHOICES = (
        ('GF', 'Gluten-Free'),
        ('VE', 'Vegan'),
    )

    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='donut_pictures')
    title = models.CharField(max_length=200)
    description = models.TextField()
    stars = models.IntegerField()
    labels = models.CharField(choices=DONUT_LABEL_CHOICES, max_length=2)
    ingredients = models.TextField()
    allergens = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("donut:donut:detail", kwargs={'pk': self.pk})


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=100)
    customer_address = models.CharField(max_length=100)
    items = models.ManyToManyField(Donut, through='OrderItem')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk}"

    def get_absolute_url(self):
        return reverse("order:order:detail", kwargs={'pk': self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    donut = models.ForeignKey('Donut', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.donut.name} for order #{self.order.pk}"




