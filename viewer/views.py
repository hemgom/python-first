import zipfile
import os

from django.http import JsonResponse

# 압축 파일 업로드
def upload_zip(request):
    if request.method == "POST" and request.FILES:
        uploaded_file = request.FILES['file']
        zip_name = uploaded_file.name

        # 업로드한 파일이 압축 파일인지 확인
        try:
            read_structure = read_zip(uploaded_file)
            response = {
                "zip_name": zip_name,
                "zip_structure": read_structure,
            }
            return JsonResponse(response, status=200)

        except zipfile.BadZipFile:
            return JsonResponse({'error': '유효하지 않은 형식의 파일'}, status=400)

    return JsonResponse({'error': '잘못된 HTTP 요청'}, status=400)

# 압축 파일 읽기
def read_zip(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as zip_contents:
        zip_structure = {"root": []}

        # 압축 파일의 디렉토리 및 파일을 하나씩 확인
        for content_info in zip_contents.infolist():
            parts = content_info.filename.split('/')    # 디렉토리 또는 파일의 경로를 분리
            current_location = zip_structure["root"]

            # 디렉토리 또는 파일의 각 경로에 따라 작업 수행
            # [경로 확인 > 'current_location' 을 지정 위치까지 이동 > 디렉토리 또는 파일 생성후 추가] 이를 반복
            for part in parts:
                if part == "":  # 만약 경로 중 빈 문자열이 있다면 다음 반복 수행
                    continue

                # 콘텐츠가 파일이고 마지막 경로라면 반복 중지
                # 파일의 경로의 마지막은 파일명이기 때문
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
                        "is_dir": True, "contents": []
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
