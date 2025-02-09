import paypalrestsdk
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from .models import Service
import json


# 🔹 Configurar PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" o "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})

# ✅ Vista de la tienda (Lista de productos)
def services(request):
    services = Service.objects.filter(available=True)
    return render(request, 'services/services.html', {'services': services})

# ✅ Agregar un producto al carrito (AJAX)
@csrf_exempt
def add_to_cart(request, service_id):
    if request.method == "POST":
        try:
            cart = request.session.get('cart', {})

            if str(service_id) in cart:
                cart[str(service_id)]["quantity"] += 1
            else:
                service = get_object_or_404(Service, id=service_id)
                cart[str(service_id)] = {
                    "title": service.title,
                    "price": float(service.price),
                    "quantity": 1,
                    "image": service.image.url
                }

            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({"success": True, "message": "✅ Producto agregado correctamente."})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"❌ Error al agregar: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

# ✅ Ver carrito de compras
# Ver carrito de compras
def view_cart(request):
    cart = request.session.get('cart', {})
    
    # 🔹 CORREGIR CÁLCULO DEL TOTAL
    total_price = sum(float(item["price"]) * int(item["quantity"]) for item in cart.values())

    return render(request, 'services/cart.html', {'cart': cart, 'total_price': total_price})


# ✅ Procesar Pago con PayPal
@csrf_exempt
def checkout(request):
    if request.method == "POST":
        try:
            cart = request.session.get('cart', {})
            total_price = sum(item["price"] * item["quantity"] for item in cart.values())

            if total_price == 0:
                return JsonResponse({"success": False, "message": "❌ No puedes pagar un carrito vacío."})

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(reverse('payment_success')),
                    "cancel_url": request.build_absolute_uri(reverse('payment_failed'))
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": "Compra en I Love Kaphíy",
                            "sku": "001",
                            "price": f"{total_price:.2f}",
                            "currency": "PEN",
                            "quantity": 1
                        }]
                    },
                    "amount": {"total": f"{total_price:.2f}", "currency": "PEN"},
                    "description": "Pago de productos en I Love Kaphíy"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.method == "REDIRECT":
                        return JsonResponse({"success": True, "redirect_url": link.href})
            return JsonResponse({"success": False, "message": "❌ Error en PayPal."})
        
        except Exception as e:
            return JsonResponse({"success": False, "message": f"❌ Error en el proceso de pago: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

# ✅ Pago con Tarjeta (Simulado)
@csrf_exempt
def process_card_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_number = data.get("card_number")
            expiry_date = data.get("expiry_date")
            cvv = data.get("cvv")
            name = data.get("name")

            # Simulación de pago aprobado si la tarjeta termina en 4
            if card_number and card_number[-1] == "4":
                return JsonResponse({"success": True, "message": "✅ Pago aprobado."})
            else:
                return JsonResponse({"success": False, "message": "❌ Pago rechazado."})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"❌ Error en el pago: {str(e)}"})

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

# ✅ Generar código QR para Yape, Plin y Agora

def generate_qr(request, payment_method):
    try:
        cart = request.session.get('cart', {})
        total_price = sum(item["price"] * item["quantity"] for item in cart.values())

        if total_price == 0:
            return HttpResponse("❌ No puedes generar un QR sin productos.", status=400)

        receiver_number = "943981389"  # Número real del receptor en Yape/Plin

        qr_urls = {
            "yape": f"yape://pay?amount={total_price:.2f}&receiver={receiver_number}",
            "plin": f"plin://pay?amount={total_price:.2f}&receiver={receiver_number}",
            "agora": f"https://www.agorapay.pe/pay/{total_price:.2f}/{receiver_number}"
        }

        qr_url = qr_urls.get(payment_method)
        if not qr_url:
            return HttpResponse("❌ Método de pago no válido", status=400)

        # Generamos el código QR
        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        return HttpResponse(buffer.getvalue(), content_type="image/png")

    except Exception as e:
        return HttpResponse(f"❌ Error al generar QR: {str(e)}", status=500)

# ✅ Página de pago exitoso
def payment_success(request):
    request.session['cart'] = {}  # Vaciar carrito después del pago
    messages.success(request, "✅ ¡Pago realizado con éxito! Gracias por tu compra.")
    return redirect(reverse('services'))

# ✅ Página de pago fallido
def payment_failed(request):
    messages.error(request, "❌ El pago no se pudo completar. Inténtalo nuevamente.")
    return redirect(reverse('view_cart'))

# ✅ Eliminar un producto del carrito
def remove_from_cart(request, service_id):
    cart = request.session.get('cart', {})

    if str(service_id) in cart:
        del cart[str(service_id)]
        request.session['cart'] = cart
        messages.success(request, "🗑 Producto eliminado del carrito.")

    return redirect(reverse('view_cart'))

# ✅ Vaciar carrito
def clear_cart(request):
    request.session['cart'] = {}
    messages.success(request, "🗑 Carrito vacío.")
    return redirect(reverse('view_cart'))

@csrf_exempt
def update_cart(request, service_id, action):
    cart = request.session.get('cart', {})

    if str(service_id) in cart:
        if action == "increase":
            cart[str(service_id)]["quantity"] += 1
        elif action == "decrease":
            if cart[str(service_id)]["quantity"] > 1:
                cart[str(service_id)]["quantity"] -= 1
            else:
                del cart[str(service_id)]  # Eliminar si la cantidad es 0

        request.session['cart'] = cart
        request.session.modified = True

        total_price = sum(item["price"] * item["quantity"] for item in cart.values())

        return JsonResponse({
            "success": True,
            "quantity": cart[str(service_id)]["quantity"] if str(service_id) in cart else 0,
            "total": cart[str(service_id)]["quantity"] * cart[str(service_id)]["price"] if str(service_id) in cart else 0,
            "cart_total": total_price
        })

    return JsonResponse({"success": False, "message": "❌ Producto no encontrado."})