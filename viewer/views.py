import os
import zipfile

from rest_framework import mixins, status, generics
from rest_framework import serializers
from rest_framework.response import Response


# 클라이언트의 JSON 타입 데이터를 Python 객체로 변환하기 위한 용도
class ZipSerializer(serializers.Serializer):
    file = serializers.FileField()

class ZipViewer(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ZipSerializer    # 직렬화 할 serializer 클래스 설정

    # POST 요청 데이터를 변환하고 유효성을 검사
    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return self.uploaded_zip(serializer)

    def perform_create(self, serializer):
        uploaded_file = serializer.validated_data['file']
        zip_name = uploaded_file.name

        try:
            read_structure = self.read_zip(uploaded_file)
            response = {
                "zip_name": zip_name,
                "zip_structure": read_structure,
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
