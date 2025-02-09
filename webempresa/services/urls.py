from django.urls import path
from .views import (
    services, add_to_cart, view_cart, update_cart, 
    checkout, process_card_payment, generate_qr,
    payment_success, payment_failed, remove_from_cart, clear_cart
)

urlpatterns = [
    path('', services, name='services'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:service_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:service_id>/<str:action>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/card/', process_card_payment, name='process_card_payment'),
    path('payment/qr/<str:payment_method>/', generate_qr, name='generate_qr'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failed/', payment_failed, name='payment_failed'),
    path('cart/remove/<int:service_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path("cart/update/<int:service_id>/<str:action>/", update_cart, name="update_cart"),
]
