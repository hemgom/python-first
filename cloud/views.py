import zipfile

from django.http import FileResponse, JsonResponse, Http404

from .models import UploadFile


def upload_file(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        original_name = file.name
        uploaded_file = UploadFile(file=file, original_name=original_name)
        uploaded_file.save()
        return JsonResponse({'message': "파일 업로드 성공!"}, status=201)

    return JsonResponse({'error': '잘못된 요청'}, status=400)


def file_list(request):
    files = UploadFile.objects.all().values('pk', 'original_name')
    return JsonResponse({'files': list(files)})


def download_file(request, pk):
    try:
        uploaded_file = UploadFile.objects.get(pk=pk)
        download_path = uploaded_file.file.path
        return FileResponse(open(download_path, 'rb'), as_attachment=True)
    except UploadFile.DoesNotExist:
        raise Http404("요청 대상 파일이 존재하지 않음")


def compression_file_contents(request, pk):
    try:
        uploaded_file = UploadFile.objects.get(pk=pk)
        zip_path = uploaded_file.file.path

        with zipfile.ZipFile(zip_path, 'r') as zip_contents:
            files = zip_contents.namelist()

        return JsonResponse({'files': list(files)})

    except UploadFile.DoesNotExist:
        raise Http404("요청 대상 파일이 존재하지 않음")

    except zipfile.BadZipFile:
        return JsonResponse({'error': "잘못된 압축 파일"}, status=400)
