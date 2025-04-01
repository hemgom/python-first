import os
import zipfile
from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import ViewerHistory
from .pagination import CustomPagination
from .serializer import ViewerHistorySerializer


class ZipViewerPost(mixins.CreateModelMixin, generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="업로드한 압축파일 구조를 읽어 출력합니다.",
        responses={200: "압축파일 구조 반환"},
        manual_parameters=[
            openapi.Parameter(
                'file', openapi.IN_FORM,
                description="업로드할 압축파일", type=openapi.TYPE_FILE
            )
        ]
    )
    def post(self, request):
        uploaded_file = request.FILES.get('file')
        zip_name = uploaded_file.name
        zip_size = uploaded_file.size

        try:
            read_structure = self.read_zip(uploaded_file)

            history = ViewerHistory.objects.create(
                file_name=zip_name,
                file_size=zip_size,
            )

            response = {
                "zip_name": zip_name,
                "zip_structure": read_structure,
                "history_id": history.id,
            }

            return Response(response, status=status.HTTP_200_OK)

        except zipfile.BadZipFile as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def read_zip(uploaded_file):
        with zipfile.ZipFile(uploaded_file, 'r') as zip_contents:
            zip_structure = {"root": []}

            for content_info in zip_contents.infolist():
                parts = content_info.filename.split('/')
                current_location = zip_structure['root']

                for part in parts:
                    if part == "":
                        continue

                    if not content_info.filename.endswith('/') and parts[-1] == part:
                        break

                    explorer = (
                        content for content in current_location
                        if content.get("dir_name") == part
                    )
                    dir_info = next(explorer, None)

                    if dir_info is None:
                        dir_info = {
                            "dir_name": part,
                            "is_dir": True,
                            "contents": []
                        }
                        current_location.append(dir_info)

                    current_location = dir_info["contents"]

                if not content_info.filename.endswith('/'):
                    file_info = {
                        "file_name": os.path.basename(content_info.filename),
                        "file_size": content_info.file_size,
                        "is_dir": False,
                    }
                    current_location.append(file_info)

        return zip_structure

class ZipViewerGet(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ViewerHistorySerializer    # 직렬화 할 serializer 클래스 설정
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="구조를 읽은 압축파일 메타정보 목록을 조회합니다.",
        responses={200: "검색 조건에 해당하는 읽은 압축파일 목록 반환"},
        manual_parameters=[
            openapi.Parameter(
                'file_name', openapi.IN_QUERY,
                description="검색조건 - 파일명", type=openapi.TYPE_STRING),
            openapi.Parameter(
                'created_at', openapi.IN_QUERY,
                description="검색조건 - 읽은 날짜(YYYY-MM-DD)", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        file_name = request.GET.get('file_name', None)
        created_at = request.GET.get('created_at', None)
        histories = ViewerHistory.objects.all()

        if file_name:
            histories = histories.filter(file_name__icontains=file_name)
        if created_at:
            try:
                valid_created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
                histories = histories.filter(created_at__gte=valid_created_at)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(histories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(histories, many=True)
        return Response(serializer.data)

class ZipViewerPatch(mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = ViewerHistory.objects.all()
    serializer_class = ViewerHistorySerializer    # 직렬화 할 serializer 클래스 설정
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="조회한 압축파일의 파일명을 수정합니다.",
        responses={200: "수정된 압축파일 정보 반환"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file_name': openapi.Schema(
                    type=openapi.TYPE_STRING, description="수정할 압축 파일명")
            }
        )
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="조회한 압축파일 정보를 삭제합니다.",
        responses={204: "반환 데이터 없음"}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
