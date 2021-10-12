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



    # Manufacture Request
    path('manufacture_req', views.manufacture_req, name='manufacture_req'),
    path('manufacture_req_detail/<int:id>/',views.manufacture_req_detail,name='manufacture_req_detail'),


    # Other
    path('profile', views.profile, name='profile'),
    path('search',views.search,name='search'),
    ]
