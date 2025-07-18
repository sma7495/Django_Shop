from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactModelForm
from .models import AboutUs, Characteristic, FAQ, TermsConditions

# website pages as class-based views
class HomePageView(TemplateView):
    template_name = 'website/index.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Add any additional context here
    #     context['featured_content'] = "Welcome to our website!"
    #     return context


class AboutPageView(TemplateView):
    template_name = 'website/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context here
        context['about_us'] = AboutUs.load()
        return context


# class ServicesPageView(ListView):
#     template_name = 'website/services.html'
#     context_object_name = 'services'

#     def get_queryset(self):
#         # Replace with your actual services data or model
#         return [
#             {'name': 'Web Development', 'description': 'Custom web solutions'},
#             {'name': 'SEO', 'description': 'Search engine optimization'},
#             {'name': 'Consulting', 'description': 'Expert advice'},
#         ]


# class PrivacyPolicyView(TemplateView):
#     template_name = 'website/privacy_policy.html'


class TermsConditionsView(TemplateView):
    template_name = 'website/terms_conditions.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context here
        context['terms'] = TermsConditions.objects.filter(is_active = True)
        context['phone'] = Characteristic.load().mobile_number
        return context

class FAQPageView(TemplateView):
    template_name = 'website/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context here
        context['faqs'] = FAQ.objects.filter(is_active = True)
        context['phone'] = Characteristic.load().mobile_number
        return context


# Error handlers (add these to your main urls.py)
# Error handlers
# handler404 = 'common.views.handler404'
# handler500 = 'common.views.handler500'

def handler404(request, exception):
    return render(request, 'website/404.html', status=404)

def handler500(request):
    return render(request, 'website/500.html', status=500)



class ContactView(FormView):
    template_name = 'website/contact.html'  # Your template path
    form_class = ContactModelForm
    success_url = reverse_lazy('website:contact')  # URL name for your contact page
    # extra_context = {'page_title': 'Contact Us'}

    def form_valid(self, form):
        # Save the contact message
        contact_message = form.save()
        
        # Send email notification if enabled
        if getattr(settings, 'SEND_CONTACT_EMAILS', False):
            self.send_contact_email(contact_message)
        
        # Add success message
        messages.success(
            self.request,
            'Your message has been sent successfully! We will get back to you soon.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Please correct the errors below.'
        )
        return super().form_invalid(form)

    def send_contact_email(self, contact_message):
        """Helper method to send contact email"""
        subject = f"New Contact Message: {contact_message.subject}"
        message = f"""
        Name: {contact_message.name}
        Email: {contact_message.email}
        Phone: {contact_message.phone_number}
        
        Message:
        {contact_message.message}
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )

    def get_context_data(self, **kwargs):
        """Add additional context to template"""
        context = super().get_context_data(**kwargs)
        # You can add more context variables here if needed
        context["info"] = Characteristic.load()
        return context