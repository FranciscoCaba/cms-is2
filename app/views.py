from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'vistas/inicio.html')

def exit(request):
    logout(request)
    return redirect('index')