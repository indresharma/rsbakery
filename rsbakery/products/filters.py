from django_filters import FilterSet


from .models import Product


class ProductFilter(FilterSet):

    class Meta:
        model = Product
        fields = {
            'product' : ['icontains'],
            'price_after_tax' : ['gte', 'lte'],
            'category__category' : ['icontains'],
            'tags__tag' : ['icontains'],
            'status' : ['iexact'],
            'product_discount' : ['gte', 'lte'],
            'weight': ['gte', 'lte'],
            'base_ingredient': ['icontains'],
        }
