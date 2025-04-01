from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from cloud.views import upload_file, file_list, download_file, compression_file_contents
from viewer.views import ZipViewerPost, ZipViewerGet, ZipViewerPatch


schema_view = get_schema_view(
    openapi.Info(
        title="Zip Viewer",
        default_version='v1',
        description="API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    # app: cloud
    path('', TemplateView.as_view(template_name='main.html'), name='main_page'),
    path('upload/', upload_file, name='upload_file'),
    path('file-list/', file_list, name='file_list'),
    path('download/<int:pk>/', download_file, name='download_file'),
    path('compression-file-contents/<int:pk>/', compression_file_contents, name='compression_file_contents'),

    # app: viewer
    path('viewer/', TemplateView.as_view(template_name='viewer.html'), name='viewer_page'),
    path('viewer/upload/', ZipViewerPost.as_view(), name='read_zip'),
    path('viewer/history/', ZipViewerGet.as_view(), name='get_viewer_history'),
    path('viewer/history/<int:pk>/', ZipViewerPatch.as_view(), name='edit_viewer_history'),

    # swagger
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
