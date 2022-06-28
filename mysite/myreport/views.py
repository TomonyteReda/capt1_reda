from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from . forms import UploadFileForm


def index(request):
    response = render(request, 'index.html')
    return response


# def handle_uploaded_file(f):


@login_required
def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('index')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {
        'form': form
    })


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # validuosim forma, tikrindami ar sutampa slaptažodžiai, ar egzistuoja vartotojas
        error = False
        if not password or password != password2:
            messages.error(request, _('Slaptažodžiai nesutampa arba neįvesti.'))
            error = True
        if not username or get_user_model().objects.filter(username=username).exists():
            messages.error(request, _('Vartotojas {} jau egzistuoja arba neįvestas.').format(username))
            error = True
        if not email or get_user_model().objects.filter(email=email).exists():
            messages.error(request, _('Vartotojas su el.praštu {} jau egzistuoja arba neįvestas.').format(email))
            error = True
        if error:
            return redirect('register')
        else:
            get_user_model().objects.create_user(username=username, email=email, password=password)
            messages.success(request, _('Vartotojas {} užregistruotas sėkmingai. Galite prisijungti').format(username))
            return redirect('index')
    return render(request, 'register.html')
