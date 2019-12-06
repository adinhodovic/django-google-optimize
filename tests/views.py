from django.shortcuts import render


def test(request):
    return render(request, "context_processors/test.html")
