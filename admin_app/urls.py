from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_create_product', views.process_create_product),
    path('select_product', views.select_product),
    path('edit_product/<int:product_id>', views.edit_product),
    path('process_product_edit/<int:product_id>', views.process_product_edit),
    path('edit_product_img/<int:product_id>', views.edit_product_img),
    path('process_add_prod_photo', views.process_add_prod_photo),
    path('delete_photo/<int:photo_id>', views.delete_photo),
    path('administrative', views.administrative),
    path('edit_user', views.edit_user),
    path('edit_user_security/<int:user_id>', views.edit_user_security),
    path('process_edit_security/<int:user_to_edit_id>', views.process_edit_security),
    path('delete_user/<int:user_id>', views.delete_user),
    path('process_add_category', views.process_add_category),
    path('edit_product_category/<int:product_id>', views.edit_product_category),
    path('process_add_product_to_category', views.process_add_product_to_category),
    path('process_remove_product_to_category', views.process_remove_product_to_category),
    path('delete_product/<int:product_id>', views.delete_product),
    path('view_quote/<int:quote_id>', views.view_quote),
    path('begin_processing_quote', views.begin_processing_quote),
    path('order_quote', views.order_quote),
    path('edit_off_notes', views.edit_off_notes),
    path('quotes_display', views.quotes_display),
    path('orders_display', views.orders_display),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),

]




