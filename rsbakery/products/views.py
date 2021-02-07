from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django_filters.views import FilterView

from .models import *
from .forms import *
from .filters import ProductFilter
from core.utils import CustomAuthMixin

############## Helper Function #######################

@login_required
def get_unit(request):
    pk = request.GET.get('pk')
    unit = RawMaterial.objects.get(id=pk).get_unit()
    return JsonResponse({'unit': unit})


# class CustomAuthMixin(LoginRequiredMixin, PermissionRequiredMixin):
#     permission_required = []


class ProductListView(FilterView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 10
    filterset_class = ProductFilter

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        if query:
            return Product.objects.filter(
                Q(product__icontains=query) | Q(category__category__icontains=query) \
                    | Q(tags__tag__icontains=query)
            ).order_by('-id')
        return Product.objects.all().order_by('-id')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)



class ProductCreateView(CustomAuthMixin, SuccessMessageMixin, CreateView):
    permission_required = ['products.add_product']
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('products:dashboard-product-add')
    success_message = 'Product added Successfully'


class ProductUpdateView(CustomAuthMixin, SuccessMessageMixin, UpdateView):
    permission_required = ['products.change_product']
    model = Product
    form_class = ProductForm
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('products:dashboard-products-list')
    success_message = 'Product updated Successfully'


class ProductDeleteView(CustomAuthMixin, DeleteView):
    permission_required = ['products.change_product']
    model = Product
    success_message = 'Product deleted Successfully'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(request, self.success_message)
        payload = {'status': True, 'message': 'Deleted'}
        return JsonResponse(payload)


#################### Dashboard Views #################################
class DashboardView(CustomAuthMixin, TemplateView):
    permission_required = ['products.access_dashboard']
    template_name = 'products/dashboard_main.html'


class DashboardProductListView(CustomAuthMixin, ProductListView):
    permission_required = ['products.access_dashboard']
    template_name = 'products/dashboard_products_list.html'
    paginate_by = 10


#################### Stock Views ######################################

class RawMaterialListView(CustomAuthMixin, ListView):
    permission_required = ['products.view_rawmaterial']
    model = RawMaterial
    template_name = 'products/dashboard_rm_list.html'
    paginate_by = 10

    def get_queryset(self):
        return RawMaterial.objects.all().order_by('-id')
  

class RawMaterialCreateView(CustomAuthMixin, SuccessMessageMixin, CreateView):
    permission_required = ['products.add_rawmaterial']
    form_class = RawMaterialForm
    template_name = 'products/dashboard_raw_material_add.html'
    success_message = 'Item added Successfully'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        html = render_to_string(self.template_name, context=context, request=request)
        return JsonResponse({'html': html})
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        messages.success(self.request, self.success_message)
        return JsonResponse({'status': True})

    def form_invalid(self, form):
        print(form.errors)
        super().form_invalid(form)


class StockListView(CustomAuthMixin, ListView):
    permission_required = ['products.view_rmstock']
    model = RMStock
    template_name = 'products/dashboard_stock_list.html'
    paginate_by = 10

    def get_queryset(self):
        return RMStock.objects.all().order_by('-id')

    
class StockCreateView(CustomAuthMixin, SuccessMessageMixin, CreateView):
    permission_required = ['products.add_rmstock']
    form_class = RMStockForm
    template_name = 'products/dashboard_stock_add.html'
    success_url = reverse_lazy('products:dashboard-stock-add')
    success_message = 'Stock added Successfully'


class StockUpdateView(CustomAuthMixin, SuccessMessageMixin, UpdateView):
    permission_required = ['products.change_rmstock']
    model = RMStock
    form_class = RMStockUpdateForm
    template_name = 'products/dashboard_stock_add.html'
    success_url = reverse_lazy('products:dashboard-stock-list')
    success_message = 'Stock updated Successfully'

class StockDeleteView(CustomAuthMixin, SuccessMessageMixin, DeleteView):
    permission_required = ['products.change_rmstock']
    model = RMStock
    success_message = 'Stock deleted Successfully'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        messages.success(request, self.success_message)
        payload = {'status': True, 'message': 'Deleted'}
        return JsonResponse(payload)


class ProductStockListView(CustomAuthMixin, ListView):
    permission_required = ['products.view_productstock']
    model = ProductStock
    template_name = 'products/dashboard_product_stock.html'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')

class ProductStockCreateView(RawMaterialCreateView):
    permission_required = ['products.add_productstock']
    form_class = ProductStockForm
    template_name = 'products/dashboard_product_stock_add.html'
    success_message = 'Item added Successfully'

