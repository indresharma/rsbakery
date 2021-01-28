from django import forms


from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            'tax': 'Tax (%)',
            'weight': 'Weight (Grams.)',
            'product_discount': 'Product Discount (%)',
            'best_before': 'Best before (In Days)',
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].required = True
        self.fields['weight'].required = True
        self.fields['price_before_tax'].required = True
        self.fields['category'].required = True
        self.fields['tax'].required = True
        self.fields['tags'].required = False
        self.fields['product_discount'].initial = 0


class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = "__all__"


class RMStockForm(forms.ModelForm):
    class Meta:
        model = RMStock
        fields = "__all__"
        widgets = {
            'validity': forms.TextInput(attrs={'type': 'date'})
        }

class RMStockUpdateForm(forms.ModelForm):
    class Meta:
        model = RMStock
        fields = "__all__"
        widgets = {
            'validity': forms.TextInput(attrs={'type': 'date'})
        }
        

    def __init__(self, *args, **kwargs):
        super(RMStockUpdateForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].disabled = True


class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = '__all__'
        labels = {
            'price': 'Price per Unit',
        }
        widgets = {
           'validity': forms.TextInput(attrs={'type': 'date'}) 
        }

    

