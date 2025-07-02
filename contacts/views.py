from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.http import HttpResponse

from contacts.forms import ContactForm
from contacts.models import Contact


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
    form = ContactForm(request.POST, request.FILES, initial={'user': request.user})

    if form.is_valid():
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
    else:
        response = render(
            request=request,
            template_name='partials/add-contact-modal.html',
            context = {
                'form': form
            }
        )
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response


@login_required
@require_http_methods(['DELETE'])
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'contact-deleted'
    return response
