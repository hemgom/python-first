from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from cloud.views import upload_file, file_list, download_file, compression_file_contents

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='main_page'),
    path('upload/', upload_file, name='upload_file'),
    path('file-list/', file_list, name='file_list'),
    path('download/<int:pk>/', download_file, name='download_file'),
    path('compression-file-contents/<int:pk>/', compression_file_contents, name='compression_file_contents'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
