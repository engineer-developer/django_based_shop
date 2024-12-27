from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(
        request,
        "requestdataapp/request-query-params.html",
        context=context,
    )


def user_form(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "requestdataapp/user-bio-form.html",
    )


FILE_MAX_SIZE = 5 * 1024 * 1024


def handle_file_upload(
    request: HttpRequest,
    max_size: int = FILE_MAX_SIZE,
) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        if myfile.size > max_size:
            return HttpResponse("File too large", status=400)
        filename = fs.save(myfile.name, myfile)
        print("saved file", filename)

    return render(
        request,
        "requestdataapp/file-upload.html",
    )
