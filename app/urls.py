from django.urls import path, re_path
from app import views

app_name='app'



urlpatterns = [
    # The home page
    path('', views.product, name='product'),
    # Product
    path('product', views.product, name='product'),
    path('product_detail/<int:id>/',views.product_detail,name='product_detail'),
    # Category
    path('category', views.category, name='category'),
    path('category_detail/<int:id>/',views.category_detail,name='category_detail'),
    # Buyers
    path('buyers', views.buyers, name='buyers'),
    path('buyer_detail/<int:id>/',views.buyer_detail,name='buyer_detail'),
    path('register_buyer', views.register_buyer, name='register_buyer'),
    # Manufacture Request
    path('purchase_request', views.purchase_request, name='purchase_request'),
    path('purchase_request_detail/<int:id>/',views.purchase_request_detail,name='purchase_request_detail'),
    # Other
    path('profile', views.profile, name='profile'),
    path('search',views.search,name='search'),
    path('register_purchase_request',views.register_purchase_request,name='register_purchase_request'),
    ]
