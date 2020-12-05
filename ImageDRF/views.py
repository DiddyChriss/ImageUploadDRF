from django.shortcuts import render



def basedview(request):
    return render(request, 'main.html')
