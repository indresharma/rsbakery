from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Q, F

from core.utils import crop_and_save

User = get_user_model()


class BaseTracker(models.Model):
    created_by = models.ForeignKey(
        User, related_name='created_%(class)s', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseStock(BaseTracker):
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    validity = models.DateField(blank=True, null=True)
    
    class Meta:
        abstract = True



class Tags(BaseTracker):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag

class Category(BaseTracker):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category


class Product(BaseTracker):
    """Finished Products available for selling"""
    product = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity_available = models.PositiveIntegerField(
        default=0, blank=True, null=True)
    price_before_tax = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    price_after_tax = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField('Tags')
    status = models.BooleanField(default=True, blank=True, null=True)
    product_discount = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(10)], blank=True, null=True)
    image = models.ImageField(upload_to='pictures',
                              default='pictures/mypic.jpg')
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    best_before = models.PositiveSmallIntegerField(blank=True, null=True)
    base_ingredient = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        if self.product:
            return self.product
        return f'Product No. {self.pk}'

    class Meta:
        permissions = (
            ('access_dashboard', 'Access Dashboard'),
        )

    def get_status(self):
        if self.status:
            return 'Active'
        return 'Disabled'

    # def get_sale_price_after_discount(self):
    #     if self.product_discount:
    #         return self.price_before_tax * (1-self.product_discount/100)
    #     return self.price_before_tax

    # def get_sale_price_after_tax(self):
    #     if self.price_before_tax:



    def save(self, *args, **kwargs):
        if self.product_discount:
            price_after_discount = self.price_before_tax * (1-self.product_discount/100)
            self.price_after_tax = price_after_discount * (1+self.tax/100)
        else:
            self.price_after_tax = self.price_before_tax * (1+self.tax/100)
        super().save(*args, **kwargs)
        image = crop_and_save(self.image.path, 350, 400)
        image.save(self.image.path)


class ProductStock(BaseStock):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_stock')

    def __str__(self):
        return str(self.product)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            Product.objects.filter(id=self.product_id).update(
                quantity_available=F('quantity_available') + self.quantity)
        super().save(*args, **kwargs)



##### Raw Materials ########

UNITS = (
    (1, 'Grams.'),
    (2, 'Pcs.'),
    (3, 'Milli-Litres.'),
    (4, 'KiloGrams.'),
    (5, 'Litres.'),
)

class RawMaterial(BaseTracker):
    item = models.CharField(max_length=25, blank=True, null=True)
    quantity_available = models.PositiveSmallIntegerField(
        blank=True, null=True)
    unit = models.PositiveSmallIntegerField(
        choices=UNITS, blank=True, null=True)

    def __str__(self):
        return self.item

    def get_unit(self):
        return self.get_unit_display()


class RMStock(BaseStock):
    PAYMENT_CHOICES = (
        ('Done', 'Done'),
        ('Pending', 'Pending'),
    )
    item = models.ForeignKey(
        'RawMaterial', on_delete=models.CASCADE, related_name='rm_stock')
    supplier = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = "Raw Material Stock"
        verbose_name_plural = "Raw Material Stock"

    def __str__(self):
        return str(self.item)

    def save(self, *args, **kwargs):
        if not self.pk:
            RawMaterial.objects.filter(id=self.item_id).update(
                quantity_available=F('quantity_available') + self.quantity)
        super().save(*args, **kwargs)
