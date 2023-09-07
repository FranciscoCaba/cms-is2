from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group, User, Permission
from .models import CustomGroup
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupCreationForm, UnsubscribeFromGroupsForm
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

def delete(request):
    obj = User.objects.get(id=request.user.id)
    obj.is_active = False
    obj.save()

    return redirect('index')

def exit(request):
    logout(request)
    return redirect('index')

def create_group(request):
    data = {
        'form': GroupCreationForm()
    }
    if request.method == 'POST':
        form = GroupCreationForm(data=request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            form.save_m2m()  
            return redirect('profile')  
        
    else:
        form = GroupCreationForm()
    
    return render(request, 'group/create_group.html', data)

def deactivate_groups(request):
    if request.method == 'POST':
        form = UnsubscribeFromGroupsForm(request.POST)
        if form.is_valid():
            group_ids_to_deactivate = form.cleaned_data.get('groups')
            CustomGroup.objects.filter(id__in=group_ids_to_deactivate).update(is_active=False)
            return redirect('profile')  
        
    else:
        form = UnsubscribeFromGroupsForm()

    groups = CustomGroup.objects.filter(is_active=True)

    return render(request, 'group/deactivate_groups.html', {'groups': groups, 'form': form})

