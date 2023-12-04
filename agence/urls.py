"""
URL configuration for agence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from voyage import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add',views.add,name='add'),
    path('hotels',views.admin_hotels_view,name='hotels'),
    path('addhotels',views.admin_add_hotel_view,name='hotel'),
    path('signup', views.customer_signup_view),
   path('login', LoginView.as_view(template_name='voyage/login.html'),name='login'),
   path('search', views.search_view,name='search'),
    path('home', views.customer_home_view,name='home'),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='voyage/adminlogin.html'),name='adminlogin'),
    path('view-customer', views.view_customer_view,name='view-customer'),
     path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
     path('my-profile', views.my_profile_view,name='my-profile'),
      path('edit-profile', views.edit_profile_view,name='edit-profile'),
     path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('delete-hotel/<int:pk>', views.delete_hotel_view,name='delete-hotel'),
    path('update-hotel/<int:pk>', views.update_hotel_view,name='update-hotel'),
     path('logout', LogoutView.as_view(template_name='voyage/logout.html'),name='logout'),
    path('accounts/profile', views.afterlogin_view,name='afterlogin'),
       path('admin-view-order', views.admin_view_order_view,name='admin-view-order'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),
    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('my-order', views.my_order_view,name='my-order'),
    path('delete-voiture/<int:pk>', views.delete_hotel_view,name='delete-voiture'),
    path('update-voiture/<int:pk>', views.update_voiture_view,name='update-voiture'),
    path('voitures',views.admin_voitures_view,name='voitures'),
    path('addvoiture',views.admin_add_voiture_view,name='voiture'),
     path('afterlogin', views.afterlogin_view,name='afterlogin'),
] 
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
