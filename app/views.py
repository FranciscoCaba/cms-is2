from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group, User
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAdminUserCreationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages


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

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

class UserCreateView(CreateView):
    model = User
    form_class = CustomAdminUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user-list')  # Redirige a la lista de usuarios después de la creación exitosa
    
    # Funcion para validar el formulario
    def form_valid(self, form):
        user = form.save()
        groups = form.cleaned_data.get('groups')
        if groups:
            user.groups.set(groups)
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user-list')  # Redirige a la lista de usuarios después de la actualización exitosa


class DesactivarUsuarioView(DetailView):
    model = User
    template_name = 'desactivar_usuario.html'  # Nombre del archivo HTML que extiende de base.html

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Cambiar el estado del usuario a inactivo
        self.object.is_active = False
        self.object.save()
        
        # Puedes agregar un mensaje de éxito si lo deseas
        messages.success(request, f"El usuario {self.object.username} ha sido desactivado.")
        return redirect('user-list')  # Cambia 'lista_usuarios' al nombre de tu vista de lista de usuarios

'''
class UserDeleteView(DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user-list')  # Redirige a la lista de usuarios después de la eliminación exitosa


    def delete(self, request, *args, **kwargs):
        # Marca al usuario como inactivo en lugar de eliminarlo
        user = self.get_object()
        user.is_active = False
        user.save()
        
        return HttpResponseRedirect(self.success_url)
'''