from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('product_lines', views.product_lines),
    path('services/<int:page_num>', views.services),
    path('view_product/<int:product_id>', views.view_product),
    path('process_add_service_to_quote', views.process_add_service_to_quote),
    path('user_account', views.user_account),
    path('request_quote', views.request_quote),
    path('process_add_item_to_quote', views.process_add_item_to_quote),
    path('add_spec_inst', views.add_spec_inst),
    path('delete_quote', views.delete_quote),
    path('increase_product_quantity', views.increase_product_quantity),
    path('decrease_product_quantity', views.decrease_product_quantity),
    path('increase_item_quantity', views.increase_item_quantity),
    path('decrease_item_quantity', views.decrease_item_quantity),
    path('remove_product_from_quote', views.remove_product_from_quote),
    path('remove_item_from_quote', views.remove_item_from_quote),
    path('submit_quote', views.submit_quote),
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