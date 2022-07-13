from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('register/', views.register, name='register'),
    path('upload-file', views.model_form_upload, name='upload'),
    path('show-report', views.model_report, name='report'),
    path('myfiles/', views.UploadedFilesByUserListView.as_view(), name='my-files'),
]
