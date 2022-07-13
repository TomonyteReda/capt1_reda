from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import DataFile, Activity
from .utils import hash_file, check_for_upload_form_error, process_load_data
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            instance.hash_checksum = hash_file(instance.file_contents)
            instance.user = request.user
            file_extension = str(file_name).split('.')[-1]
            status = check_for_upload_form_error(request, form, instance, file_name, file_extension)
            if status == 'error':
                return render(request, 'upload_file.html', {
                    'form': form
                })
            else:
                instance.save()
                process_load_data(request, instance, file_name, file_extension)
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
    query_set = Activity.objects.filter(user=request.user)
    result = query_set.values('log_date', 'data_file__upload_date')\
        .order_by('log_date')\
        .annotate(impressions=Sum('quantity_impressions'), clicks=Sum('quantity_clicks'))
    total_impressions = query_set.aggregate(Sum('quantity_impressions'))['quantity_impressions__sum']
    total_clicks = query_set.aggregate(Sum('quantity_clicks'))['quantity_clicks__sum']
    page = request.GET.get('page')
    paginator = Paginator(result, 50)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    context = {
        'report': result,
        'total_impressions': total_impressions,
        'total_clicks': total_clicks
    }
    return render(request, 'report.html', context=context)


class UploadedFilesByUserListView(LoginRequiredMixin, generic.ListView):
    model = DataFile
    context_object_name = 'files'
    template_name = 'user_files.html'
    paginate_by = 5

    def get_queryset(self):
        return DataFile.objects.filter(user=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
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
