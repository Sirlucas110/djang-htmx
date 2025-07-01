from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from contacts.forms import ContactForm


@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {
        'contacts': contacts,
        'form': ContactForm()
    }
    return render(request, 'contacts.html', context)


def search_contacts(request):
    consulta = request.GET.get('search', '')

    # use a consulta para filtrar contatos por nome ou e-mail
    contacts = request.user.contacts.filter(
        Q(name__icontains=consulta) | Q(email__icontains=consulta)
    )

    return render(
        request=request,
        template_name='partials/contact-list.html',
        context = {
            'contacts': contacts
        }
    )

@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST)
    if form.is_valid:
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
    
    response = render(
        request=request,
        template_name='partials/contact-row.html',
        context = {
            'contact': contact
        }
    )
    response['HX-Trigger'] = 'success'

    return response

