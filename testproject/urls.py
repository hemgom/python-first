from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from cloud.views import upload_file, file_list, download_file, compression_file_contents
from viewer.views import upload_zip

urlpatterns = [
    # app: cloud
    path('', TemplateView.as_view(template_name='main.html'), name='main_page'),
    path('upload/', upload_file, name='upload_file'),
    path('file-list/', file_list, name='file_list'),
    path('download/<int:pk>/', download_file, name='download_file'),
    path('compression-file-contents/<int:pk>/', compression_file_contents, name='compression_file_contents'),

    # app: viewer
    path('viewer/', TemplateView.as_view(template_name='viewer.html'), name='viewer_page'),
    path('viewer/upload/', upload_zip, name='upload_zip'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
