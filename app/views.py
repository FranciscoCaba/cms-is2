from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import logout

# Create your views here.
class CustomTemplateView(TemplateView):
    group_name= None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        if user.is_authenticated:
            group= Group.objects.filter(user=user).first()
            if group:
                self.group_name=group.name
        context['group_name'] = self.group_name
        return context
    
class ProfileView(CustomTemplateView):
    template_name= 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user=self.request.user
        return context
    
class IndexView(CustomTemplateView):
    template_name= 'vistas/inicio.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user=self.request.user
        return context
    
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    return render(request, 'registration/register.html', data)

def edit(request):
    data = {
        'form': CustomUserChangeForm(instance=request.user)
    }

    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    return render(request, 'vistas/edit.html', data)

def exit(request):
    logout(request)
    return redirect('index')
