from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
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
      
def index(request):
    return render(request, 'vistas/inicio.html')
      
def exit(request):
    logout(request)
    return redirect('index')
