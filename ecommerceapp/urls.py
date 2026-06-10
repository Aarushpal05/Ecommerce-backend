from django.urls import path
from . import views 
# from .views import login_view, logout_view
 

urlpatterns=[
    path('',views.home, name='home'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('addcategory', views.addcategory, name='addcategory'),
    path('product_list', views.product_list, name='product_list'),
    path('category_list',views.category_list,name='category_list'),
    path('deletecategory/<int:id>/', views.delete_category),
    path('updatecategory/<int:id>/', views.update_category, name='update_category'),
    path('updateproduct/<int:id>', views.editProduct),
    path('deleteproduct/<int:id>',views.deleteproduct),
    path('login/',views.login_view, name='loginadmin'),
    path('logout/',views.logout_view, name='logout'),
    path('order_list/', views.order_view, name='order_list'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),
    path('order_item/<int:id>/', views.order_item, name='order_item'),

    path('api/register/', views.signupAPI),
    path('api/login/', views.loginAPI),
    path('api/products/', views.product_list_api, name='productlistapi'),
    path('api/categories/', views.category_list_api, name='categorylistapi'),
    path('api/products/<int:id>/', views.product_detail),
    path('api/profile/', views.profile_view),
    path('api/category_products/<int:category_id>/', views.Productsbycategory),
    path('api/add-to-cart/', views.add_to_cart),
    path('api/cart/', views.view_cart, name='view_cart'),
     path('api/cart/update/<int:pk>/', views.update_cart),
    path('api/cart/delete/<int:pk>/', views.delete_cart),       
    path('api/orders/history/', views.user_order_history),
    path('api/create-order/', views.create_order),

    
]