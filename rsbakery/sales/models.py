from django.db import models
from django.contrib.auth import get_user_model

from products.models import BaseTracker

User = get_user_model()


class OrderItem(BaseTracker):
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_item')
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    price_before_tax = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    price_after_tax = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    product_discount = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price_before_tax = self.item.price_before_tax
            self.tax = self.item.tax
            self.price_after_tax = self.item.price_after_tax
            self.product_discount = self.item.product_discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} of {self.item.product}'

    def get_total_item_price(self):
        """Returns total item price after discount and tax"""
        return self.quantity * self.price_after_tax

    def get_total_item_price_before_tax(self):
        """Returns total item price before discount and tax"""
        return self.quantity * self.price_before_tax

class Order(BaseTracker):
    customer = models.CharField(max_length=25, blank=True, null=True)
    customer_phone = models.CharField(max_length=10, blank=True, null=True)
    item = models.ManyToManyField('OrderItem')
    ordered = models.BooleanField(default=False)
    total_order_value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        """Gets grand order total"""
        self.total_order_value=0
        for order_item in self.item.all():
            self.total_order_value+= order_item.get_total_item_price()
        self.save()
        return self.total_order_value

    def get_total_price_before_tax(self):
        """Gets order total before tax"""
        total_price_before_tax=0
        for order_item in self.item.all():
            total_price_before_tax+= order_item.get_total_item_price_before_tax()
        return total_price_before_tax

    def get_total_tax(self):
        """Returns Total Tax"""
        total_tax = self.get_total_price() - self.get_total_price_before_tax()
        return total_tax

    def get_items(self):
        items = ''
        for item in self.item.all():
            items += f'{item}, '
            
        return items


class Invoices(BaseTracker):
    pass