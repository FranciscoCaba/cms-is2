from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import Group, User
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAdminUserCreationForm, CustomAdminUserChangeForm, GroupCreationForm, GroupEditForm
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Count, Q, Value
from contenido.models import Categoria, Contenido
from django.db.models.functions import Cast



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
        context['categorias']=Categoria.objects.filter(is_active=True).annotate(num_contenidos=Count('categoria',
        filter=Q(categoria__estado='Publicado', categoria__is_active=True)))
        if(user.is_authenticated): 
            context['categorias_favoritas'] = user.categoria_favoritos.all().annotate(num_contenidos=Count('categoria',
            filter=Q(categoria__estado='Publicado', categoria__is_active=True)))
            context['contenidos'] = Contenido.objects.filter(estado='Publicado', is_active=True, categoria__is_active=True).order_by('-fecha')
        else:
            context['contenidos'] = Contenido.objects.filter(estado='Publicado', solo_suscriptores=False, is_active=True, categoria__is_active=True).order_by('-fecha')
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

@permission_required('auth.add_group')
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
            return redirect('group_list')  
        
    else:
        form = GroupCreationForm()
    
    return render(request, 'group/create_group.html', data)

@permission_required('auth.delete_group')
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST' and 'delete_group' in request.POST:
        group.delete()
        return redirect('group_list')

    groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})

@permission_required('auth.change_group')
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    
    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupEditForm(instance=group)
    
    return render(request, 'group/edit_group.html', {'form': form, 'group': group})

@permission_required('auth.view_group')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group/group_list.html', {'groups': groups})


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

class UserCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.add_user'
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


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    form_class = CustomAdminUserChangeForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user-list')  # Redirige a la lista de usuarios después de la actualización exitosa


class DesactivarUsuarioView(PermissionRequiredMixin, DetailView):
    permission_required = 'auth.delete_user'
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

class ActivarUsuarioView(PermissionRequiredMixin, DetailView):
    permission_required = 'auth.delete_user'
    model = User
    template_name = 'activar_usuario.html'  # Nombre del archivo HTML que extiende de base.html

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Cambiar el estado del usuario a activo
        self.object.is_active = True
        self.object.save()
        
        # Puedes agregar un mensaje de éxito si lo deseas
        messages.success(request, f"El usuario {self.object.username} ha sido activado.")
        return redirect('user-list')  # Cambia 'lista_usuarios' al nombre de tu vista de lista de usuarios
    
class PaginaNoEncontradaView(View):
    def get(self, request):
        return render(request, 'no_encontrada.html')
    

def resultados_busqueda(request):
    query = request.GET.get('q')
    modo = request.GET.get('busqueda')
    print(modo)
    contenidos = ()
    categorias = ()
    usuarios = ()

    if query:
        if modo == 'contenido':
            contenidos = Contenido.objects.filter(
                Q(titulo__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(resumen__icontains=query), is_active=True).distinct()
        elif modo == 'categoria':
            categorias = Categoria.objects.filter(
                Q(nombre__icontains=query), is_active=True).distinct()
        elif modo == 'usuario':
            usuarios = User.objects.filter(
                Q(username__icontains=query), is_active=True).distinct()
        else:
            contenidos = Contenido.objects.filter(
                Q(titulo__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(resumen__icontains=query) |
                Q(categoria__nombre__icontains=query) |
                Q(user__username__icontains=query), is_active=True).distinct()
    else:
        query = ''

    return render(request, 'busqueda/resultado.html', {'contenidos': contenidos, 'categorias': categorias, 'usuarios': usuarios, 'query': query})