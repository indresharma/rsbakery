from django_filters import FilterSet


from .models import Product


class ProductFilter(FilterSet):

    class Meta:
        model = Product
        fields = {
            'price_after_tax' : ['gte', 'lte'],
            'category' : ['exact'],
            'product_discount' : ['gte', 'lte'],
            'weight': ['gte', 'lte'],
            'base_ingredient': ['icontains'],
        }
