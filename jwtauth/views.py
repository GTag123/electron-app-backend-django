from django.http import HttpResponse
def mainPage(request):
    return HttpResponse(
        """Хай!<br>
        <a href="https://github.com/GTag123/electron-app-frontend">Репозиторий проекта</a>""",
        status=202)