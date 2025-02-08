from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']  # Nombre del usuario
            email = contact_form.cleaned_data['email']
            content = contact_form.cleaned_data['content']

            # 📩 **Correo al Administrador**
            admin_email = EmailMessage(
                subject="I love kaphiy: Nuevo Mensaje de Contacto",
                body=f"De {name} <{email}>\n\nMensaje:\n\n{content}",
                from_email=f"{name} <{email}>",  # Muestra el nombre del usuario en el remitente
                to=["ilovekaphiy@gmail.com"],  # Cambia por tu correo de administración
                reply_to=[email]
            )

            # 📩 **Correo de Confirmación al Usuario**
            user_email = EmailMessage(
                subject="I love kaphiy - Confirmación de Contacto",
                body=f"Hola {name},\n\nHemos recibido tu mensaje y te responderemos pronto.\n\nGracias por contactarnos.\n\nSaludos,\nI love kaphiy ☕",
                from_email="I love Kaphíy <ilovekaphiy@gmail.com>",  # Aquí aparece el nombre de la empresa
                to=[email],  # Se envía al usuario
                reply_to=["ilovekaphiy@gmail.com"]   # Cambia por tu correo
            )

            try:
                admin_email.send()  # Envía al administrador
                user_email.send()  # Envía al usuario
                messages.success(request, "¡Tu mensaje ha sido enviado con éxito! Revisa tu correo para la confirmación.")
                return redirect(reverse('contact'))
            except Exception as e:
                messages.error(request, "Hubo un error al enviar el mensaje. Inténtalo de nuevo más tarde.")
                print(f"Error al enviar el correo: {e}")

    return render(request, 'contact/contact.html', {'form': contact_form})


