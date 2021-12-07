from django.urls import path
from . import views


app_name = 'accounts'


urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    # wishlist
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/add_to_wishlist/<int:id>', views.add_to_wishlist, name='add_product_to_wishlist'),
    path('wishlist/remove_wishlist_product/<int:_id>', views.remove_wishlist_product, name='remove_wishlist_product'),


]