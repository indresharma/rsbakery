import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, View
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


from .models import *
# from .forms import *

from products.models import Product

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs.get('pk'))

        data = {
            'order': order,
        }
        pdf = render_to_pdf('sales/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

################ ------------------------- ##############################


def get_price(request):
    price = get_object_or_404(Product, id=request.GET.get('id')).price_after_tax
    return JsonResponse({'price': price})


class CustomAuthMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = []


class OrderCreateView(CustomAuthMixin, View):
    template_name = 'sales/add_sales.html'
    tax = 18

    def get(self, request, *args, **kwargs):
        items = Product.objects.all()
        return render(request, self.template_name, context={'items': items})

    def post(self, request, *args, **kwargs):
        items = request.POST.getlist('item')
        qty_list = request.POST.getlist('quantity')
        # total_order_value = request.POST.get('total_order_value')
        customer = request.POST.get('customer', '')
        customer_phone = request.POST.get('customer_phone', '')
        order = Order.objects.create(
            created_by=request.user, 
            # total_order_value=total_order_value,
            customer = customer,
            customer_phone=customer_phone,
            ordered=True
        )
        for i in range(len(items)):
            product = Product.objects.get(id=items[i])
            order_item = OrderItem.objects.create(
                item=product,
                quantity=qty_list[i],
                ordered=True
            )
            order.item.add(order_item)
            order.save()

        return redirect('sales:get_invoice', order.id)

        return render(request, self.template_name, context={'items': items})


class OrdersListView(ListView):
    model = Order
    template_name = 'sales/orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')