from django.shortcuts import render


def landing(request):
    return render(request, 'public/landing.html')


def info(request):
    return render(request, 'public/info.html')


def abstract(request):
    return render(request, 'public/abstract.html')


def algorithm(request):
    return render(request, 'public/algorithm.html')


def example(request):
    return render(request, 'public/example.html')


def homepage(request):
    return render(request, 'public/homepage.html')
