from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import ContactForm

def contact(request):
    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email_user = contact_form.cleaned_data['email']
            content = contact_form.cleaned_data['content']

            # 📩 **Correo al Administrador**
            admin_email = EmailMessage(
                subject="I Love Kaphíy: Nuevo Mensaje de Contacto",
                body=f"De {name} <{email_user}>\n\nMensaje:\n\n{content}",
                from_email=f"{name} <{email_user}>",
                to=["ilovekaphiy@gmail.com"],  # Cambia por tu correo de administración
                reply_to=[email_user]
            )

            # 📩 **Correo de Confirmación al Usuario (HTML con banner)**
            email_html = render_to_string('emails/confirmation_email.html', {
                'name': name,
                'message': content
            })

            user_email = EmailMessage(
                subject="I Love Kaphíy - Confirmación de Contacto",
                body=email_html,
                from_email="I Love Kaphíy <ilovekaphiy@gmail.com>",
                to=[email_user],
                reply_to=["ilovekaphiy@gmail.com"]
            )
            user_email.content_subtype = "html"  # Indicar que el contenido es HTML

            try:
                admin_email.send()  # Envía al administrador
                user_email.send()  # Envía al usuario con el banner
                messages.success(request, "¡Tu mensaje ha sido enviado con éxito! Revisa tu correo para la confirmación.")
                return redirect(reverse('contact'))
            except Exception as e:
                messages.error(request, "Hubo un error al enviar el mensaje. Inténtalo de nuevo más tarde.")
                print(f"Error al enviar el correo: {e}")

    return render(request, 'contact/contact.html', {'form': contact_form})
