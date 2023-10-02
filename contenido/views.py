from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import ContenidoForm, CategoriaForm, CategoriaEditForm, ContenidoEditForm, BorradorEditForm, VersionContenidoEditForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Categoria, Contenido, Like,VersionContenido
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

class ContenidoFormView(PermissionRequiredMixin, CreateView):
    permission_required = 'contenido.add_contenido'
    template_name = 'contenido/contenido_crear.html'
    form_class = ContenidoForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'
        else:
            form.instance.estado = 'En revisión'
        return super(ContenidoFormView,self).form_valid(form)
    
    def get_success_url(self):
        if self.object.estado == 'Borrador':
            return reverse_lazy('borradores_lista')  # Reemplaza 'borrador-lista' con tu nombre de URL correcto
        else:
            return reverse_lazy('index')  # Reemplaza 'index' con tu nombre de URL correcto

class CategoriaFormView(PermissionRequiredMixin, CreateView):
    permission_required = 'contenido.add_categoria'
    template_name = 'categoria/categoria_crear.html'
    form_class = CategoriaForm
    success_url = '/contenido/categoria'

    def form_valid(self, form):
        return super(CategoriaFormView,self).form_valid(form)

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'categoria/categoria_detail.html'
    context_object_name = 'categoria'

class CategoriaUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'contenido.change_categoria'
    model = Categoria
    form_class = CategoriaEditForm
    template_name = 'categoria/categoria_edit.html'
    success_url = reverse_lazy('categoria-list')

class DesactivarCategoriaView(PermissionRequiredMixin, DetailView):
    permission_required = 'contenido.delete_categoria'
    model = Categoria
    template_name = 'categoria/desactivar_categoria.html'  # Nombre del archivo HTML que extiende de base.html

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Cambiar el estado de la categoria a inactivo
        self.object.is_active = False
        self.object.save()

        return redirect('categoria-list')

class ActivarCategoriaView(PermissionRequiredMixin, DetailView):
    permission_required = 'contenido.delete_categoria'
    model = Categoria
    template_name = 'categoria/activar_categoria.html'  # Nombre del archivo HTML que extiende de base.html

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Cambiar el estado de la categoria a activo
        self.object.is_active = True
        self.object.save()

        return redirect('categoria-list')
    
# Vista de contenidos por categoria
class MostrarContenidosView(View):
    template_name = 'mostrar_contenidos.html'

    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        contenidos = Contenido.objects.filter(categoria=categoria, is_active=True, estado='Publicado').order_by('-fecha')
        context = {'categoria': categoria, 'contenidos': contenidos}
        return render(request, self.template_name, context)
    

class ListarRevisionesView(ListView):
    model = Contenido
    template_name = 'listar_revisiones.html'
    context_object_name = 'borradores'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión').order_by('-fecha')
    
def publicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    # Cambiar el estado del contenido a "Publicado"
    contenido.estado = 'Publicado'
    contenido.save()

    # Redirigir a la lista de borradores
    return redirect('revisar')

def rechazar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    # Cambiar el estado del contenido a "Rechazado"
    contenido.estado = 'Rechazado'
    contenido.save()

    # Redirigir a la lista de borradores
    return redirect('revisar')

class ContenidoBorradorListView(LoginRequiredMixin, ListView):
    model = Contenido
    template_name = 'borrador/borradores_lista.html'
    context_object_name = 'contenidos_borrador'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Borrador').order_by('-fecha')

class ContenidoRechazadoListView(LoginRequiredMixin, ListView):
    model = Contenido
    template_name = 'contenido/rechazados_lista.html'
    context_object_name = 'contenidos_rechazados'

    def get_queryset(self):
        # Obtener los contenidos en estado "rechazado" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Rechazado').order_by('-fecha')

def detalle_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.user.is_authenticated:
        user_likes_contenido = request.user.contenido_likes.filter(id=contenido.id).exists()
    else:
        user_likes_contenido = False
    
    return render(request, 'contenido/contenido_detalle.html', {'contenido': contenido, 'user_likes_contenido': user_likes_contenido})

def toggle_like(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)

    if request.user.is_authenticated:
        try:
            # Intenta obtener el like existente del usuario para este contenido
            like = Like.objects.get(contenido=contenido, user=request.user)
            # Si el like existe, elimínalo (quitar like)
            like.delete()
            messages.success(request, 'Like eliminado correctamente.')
        except Like.DoesNotExist:
            # Si el like no existe, créalo (dar like)
            Like.objects.create(contenido=contenido, user=request.user)
            messages.success(request, 'Like agregado correctamente.')
        
        # No es necesario incrementar/decrementar el contador de likes aquí

        return redirect('detalle_contenido', pk=contenido.id)
    else:
        messages.error(request, 'Debes estar autenticado para dar/quitar like.')
        return redirect('detalle_contenido', pk=contenido.id)
    
class EditarContenidoView(UpdateView):
    model = Contenido
    form_class = ContenidoEditForm
    template_name = 'contenido/contenido_editar.html'
    success_url = reverse_lazy('index')

class EditarBorradorView(UpdateView):
    model = Contenido
    form_class = BorradorEditForm
    template_name = 'borrador/borrador_editar.html'
    success_url = reverse_lazy('borradores_lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'
        else:
            form.instance.estado = 'En revisión'
        return super(EditarBorradorView,self).form_valid(form)

def detalle_autor(request, pk):
    # Obtiene el usuario (autor) por su clave primaria (pk)
    autor = get_object_or_404(User, pk=pk)

    # Obtiene los contenidos relacionados al autor
    contenidos = Contenido.objects.filter(user=autor).order_by('-fecha')

    # Renderiza el template para mostrar los detalles del autor y sus contenidos
    return render(request, 'autor/contenidos_autor.html', {'autor': autor, 'contenidos': contenidos})

@login_required
def kanban_view(request):
    if request.user.is_staff:
        contexto={'contenidos': Contenido.objects.all().order_by('-fecha')}
    else:
        contexto={'contenidos': Contenido.objects.filter(user=request.user).order_by('-fecha')}
    return render(request, 'kanban.html', contexto)

class ContenidoVersionListView(LoginRequiredMixin, ListView):
    model = VersionContenido
    template_name = 'version/version_lista.html'
    context_object_name = 'version_contenidos'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return VersionContenido.objects.all().order_by('-titulo')
    


def editar_version(request, version_id):
    version = get_object_or_404(VersionContenido, pk=version_id)
    
    if request.method == 'POST':
        form = VersionContenidoEditForm(request.POST, instance=version)
        if form.is_valid():
            nueva_version = form.save(commit=False)
            nueva_version.pk = None  # Crear una nueva instancia de VersionContenido
            nueva_version.user_modificacion = request.user
            nueva_version.save()
            return redirect(reverse_lazy('contenido-version'))  # Redirigir a la lista de versiones
    else:
        form = VersionContenidoEditForm(instance=version)
    
    return render(request, 'version/version_editar.html', {'form': form, 'version': version})