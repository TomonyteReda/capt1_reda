from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import DataFile, Activity
import base64
from .process_data import add_data_from_file_to_db
from django.db.models import Sum
import pandas as pd
import numpy as np


def index(request):
    num_users = get_user_model().objects.all().count()
    context = {
        'num_users': num_users,
    }
    response = render(request, 'index.html', context=context)
    return response


@login_required
def model_form_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.instance
            instance.file_contents = request.FILES['file_contents']
            file_name = instance.file_contents.name
            instance.hash_checksum = base64.b64encode(file_name.encode())
            instance.user = request.user
            if DataFile.objects.filter(user=instance.user, hash_checksum=instance.hash_checksum).count() >= 1:
                messages.error(request, _('file {} is already uploaded').format(file_name))
                return render(request, 'upload_file.html', {
                    'form': form
                })
            else:
                instance.save()
                add_data_from_file_to_db(file_contents=instance.file_contents,
                                         file_name=file_name,
                                         user=instance.user,
                                         instance=instance)
                messages.success(request, _('file {} uploaded successfully!').format(file_name))
                return render(request, 'upload_file.html', {
                    'form': form
                })
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {
        'form': form
    })


@login_required
def model_report(request):
    data = Activity.objects.filter(user=request.user).values('log_date', 'activity_type', 'quantity', 'upload_date')
    pivot = pd.pivot_table(data, values=['quantity'], index=['log_date', 'upload_date'],
                           columns=['activity_type'], aggfunc=np.sum, fill_value=0)
    context = {
        'Report': pivot.to_html,
               }
    return render(request, 'user_activity_report.html', context)


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
            messages.error(request, _('passwords do not match'))
            error = True
        if not username or get_user_model().objects.filter(username=username).exists():
            messages.error(request, _('user {} already registered').format(username))
            error = True
        if not email or get_user_model().objects.filter(email=email).exists():
            messages.error(request, _('email {} already exists').format(email))
            error = True
        if error:
            return redirect('register')
        else:
            get_user_model().objects.create_user(username=username, email=email, password=password)
            messages.success(request, _('user {} registered successfully').format(username))
            return redirect('index')
    return render(request, 'register.html')
