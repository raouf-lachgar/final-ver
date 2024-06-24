from django.urls import path
from . import views
from .views import index, submit_product_view

urlpatterns = [
    path("", views.index, name="index"),
    #path("search",views.search,name="search"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("sign", views.sign_view, name="sign"),
    path('submit/', submit_product_view, name='submit_product'),
    path('profile/', views.profile_view, name='profile'),
     path('profile/update', views.profileUpdate_view, name='update'),
     path('profile/delete', views.userDelete_view, name='delete'),
    path('delete/<int:product_id>/', views.delete_product_view, name='delete_product'),
      path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
      path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
      path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
       path('remove_saved_product/<int:product_id>/', views.remove_saved_product, name='remove_saved_product'),
        path('save_product/<int:product_id>/', views.save_product, name='save_product'),
        path('product/<int:product_id>/buy/', views.buy_product, name='buy_product'),
         path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
         path('product/<int:product_id>/orders/', views.product_orders, name='product_orders'),
         path('subscribe/', views.subscribe_view, name='subscribe'),
         path('cart/', views.cart_view, name='cart'),

      
]