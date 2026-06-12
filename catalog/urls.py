from django.urls import path
from . import views

#aggiorno i patterns ogni vista che creo
urlpatterns = [
    # --- PRODOTTI ---
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # --- CARRELLO ---
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # --- ORDINI ---
    path('order/create/', views.order_create, name='order_create'),
    path('my-orders/', views.CustomerOrderListView.as_view(), name='my_orders'),
    path('manage/orders/', views.ManagerOrderListView.as_view(), name='manage_orders'),
]