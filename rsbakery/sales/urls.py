from django.urls import path


from .views import *

app_name = 'sales'

urlpatterns = [
    path('billing/', OrderCreateView.as_view(), name="billing"),
    path('orders/', OrdersListView.as_view(), name="orders"),

    path('get_price/', get_price, name="get_price"),
    path('get_invoice/<int:pk>/', GeneratePdf.as_view(), name="get_invoice"),

]