from django.urls import path


from .views import *

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(), name="products"),

    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('dashboard/products/', DashboardProductListView.as_view(), name="dashboard-products-list"),
    path('dashboard/products/add/', ProductCreateView.as_view(), name="dashboard-product-add"),
    path('dashboard/products/update/<int:pk>/', ProductUpdateView.as_view(), name="dashboard-product-update"),
    path('dashboard/products/delete/<int:pk>/', ProductDeleteView.as_view(), name="dashboard-product-delete"),

    path('dashboard/raw_material/', RawMaterialListView.as_view(), name="dashboard-raw-material-list"),
    path('dashboard/raw_material/add/', RawMaterialCreateView.as_view(), name="dashboard-raw-material-add"),
    # path('dashboard/raw_material/update/<int:pk>/', RawMaterialUpdateView.as_view(), name="dashboard-raw-material-update"),

    path('dashboard/stock/', StockListView.as_view(), name="dashboard-stock-list"),
    path('dashboard/stock/add/', StockCreateView.as_view(), name="dashboard-stock-add"),
    path('dashboard/stock/update/<int:pk>/', StockUpdateView.as_view(), name="dashboard-stock-update"),
    path('dashboard/stock/delete/<int:pk>/', StockDeleteView.as_view(), name="dashboard-stock-delete"),

    path('dashboard/products/stock/', ProductStockListView.as_view(), name="dashboard-product-stock-list"),
    path('dashboard/products/stock/add/', ProductStockCreateView.as_view(), name="dashboard-product-stock-add"),

    path('get_unit/', get_unit, name="get_unit"),
]