import os
import zipfile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ZipViewer(APIView):
    def post(self, request):
        return self.upload_zip(request)

    def upload_zip(self, request):
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            zip_name = uploaded_file.name

            try:
                read_structure = self.read_zip(uploaded_file)
                response = {
                    "zip_name": zip_name,
                    "zip_structure": read_structure,
                }
                return Response(response, status=status.HTTP_200_OK)

            except zipfile.BadZipFile as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "잘못된 HTTP 요청"}, status=status.HTTP_400_BAD_REQUEST)

    # 'read_zip' 메서드가 ZipViewer 클래스의 필드나 메서드를 사용하지 않기에 static 메서드로 작성(변경)
    @staticmethod
    def read_zip(uploaded_file):
        with zipfile.ZipFile(uploaded_file, 'r') as zip_contents:
            zip_structure = {"root": []}

            for content_info in zip_contents.infolist():
                parts = content_info.filename.split('/')
                current_location = zip_structure["root"]

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
