from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_create_product', views.process_create_product),
    path('select_product/<int:page_num>', views.select_product),
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
    path('process_delete_category', views.process_delete_category),
    path('edit_product_category/<int:product_id>', views.edit_product_category),
    path('process_add_product_to_category', views.process_add_product_to_category),
    path('process_remove_product_to_category', views.process_remove_product_to_category),
    path('delete_product/<int:product_id>', views.delete_product),
    path('view_quote/<int:quote_id>', views.view_quote),
    path('view_order/<int:order_id>', views.view_order),
    path('begin_processing_quote', views.begin_processing_quote),
    path('increase_product_quantity', views.increase_product_quantity),
    path('decrease_product_quantity', views.decrease_product_quantity),
    path('increase_item_quantity', views.increase_item_quantity),
    path('decrease_item_quantity', views.decrease_item_quantity),
    path('increase_adminitem_quantity', views.increase_adminitem_quantity),
    path('decrease_adminitem_quantity', views.decrease_adminitem_quantity),
    path('remove_product_from_quote', views.remove_product_from_quote),
    path('remove_item_from_quote', views.remove_item_from_quote),
    path('remove_adminitem_from_quote', views.remove_adminitem_from_quote),
    path('process_add_adminitem_to_quote', views.process_add_adminitem_to_quote),
    path('order_quote', views.order_quote),
    path('order_increase_product_quantity', views.order_increase_product_quantity),
    path('order_decrease_product_quantity', views.order_decrease_product_quantity),
    path('order_remove_product_from_order', views.order_remove_product_from_order),
    path('order_increase_item_quantity', views.order_increase_item_quantity),
    path('order_decrease_item_quantity', views.order_decrease_item_quantity),
    path('order_remove_item_from_order', views.order_remove_item_from_order),
    path('order_increase_adminitem_quantity', views.order_increase_adminitem_quantity),
    path('order_decrease_adminitem_quantity', views.order_decrease_adminitem_quantity),
    path('remove_adminitem_from_order', views.remove_adminitem_from_order),
    path('begin_processing_order', views.begin_processing_order),
    path('process_add_adminitem_to_order', views.process_add_adminitem_to_order),
    path('edit_order_off_notes', views.edit_order_off_notes),
    path('attach_new_order', views.attach_new_order),
    path('build_attached_order', views.build_attached_order),
    path('process_attach_order', views.process_attach_order),
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
    path('edit_off_notes', views.edit_off_notes),
    path('quotes_display/<int:page_num>', views.quotes_display),
    path('completed_quotes_display/<int:page_num>', views.completed_quotes_display),
    path('orders_display/<int:page_num>', views.orders_display),
    path('completed_orders_display/<int:page_num>', views.completed_orders_display),
    path('confirm_delete_quote/<int:quote_id>', views.confirm_delete_quote),
    path('confirm_delete_order/<int:order_id>', views.confirm_delete_order),
    path('delete_quote', views.delete_quote),
    path('delete_order', views.delete_order),
    path('find_quote', views.find_quote),
    path('find_order', views.find_order),
    path('build_quote', views.build_quote),
    path('select_quote_user', views.select_quote_user),
    path('select_quote_contact', views.select_quote_contact),
    path('process_build_quote', views.process_build_quote),
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
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),
    # path('logout', views.logout),

]




