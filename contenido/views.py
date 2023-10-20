from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import ContenidoForm, CategoriaForm, CategoriaEditForm, ContenidoEditForm, BorradorEditForm, RechazadoEditForm, VersionContenidoEditForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Categoria, Contenido, Like,VersionContenido, Image, Video
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

class ContenidoFormView(PermissionRequiredMixin, CreateView):
    permission_required = 'contenido.add_contenido'
    template_name = 'contenido/contenido_crear.html'
    form_class = ContenidoForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if  'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                form.instance.estado = 'En revisión'
                context = {
                    'titulo': form.instance.titulo,      
                }      
                message = strip_tags(render_to_string('notificaciones/en_revision.html', context))
                send_mail('Cambio de estado de publicacion',message,'cmsis2eq01@gmail.com',[self.request.user.email], fail_silently=False)
            else:
                form.instance.estado = 'Publicado'
                context = {
                    'titulo': form.instance.titulo,      
                }      
                message = strip_tags(render_to_string('notificaciones/publicado.html', context))
                send_mail('Cambio de estado de publicacion',message,'cmsis2eq01@gmail.com',[self.request.user.email], fail_silently=False)
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'
        contenido = form.save(commit=False)
        contenido.save(user=self.request.user)
        if 'borradorcito' in self.request.POST:
            context = {
                    'titulo': form.instance.titulo,      
                }      
            message = strip_tags(render_to_string('notificaciones/borrador.html', context))
            send_mail('Cambio de estado de publicacion',message,'cmsis2eq01@gmail.com',[self.request.user.email], fail_silently=False)
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=contenido, image=image)
        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=contenido, video=video)
        return redirect('/')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
    

class ListarRevisionesView(PermissionRequiredMixin,ListView):
    model = Contenido
    permission_required = 'contenido.ver_revisiones'
    template_name = 'listar_revisiones.html'
    context_object_name = 'por_revisar'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión').order_by('-fecha')
    
class ListarUnaRevisionView(PermissionRequiredMixin,ListView):
    model = Contenido
    permission_required = 'contenido.ver_revisiones'
    template_name = 'listar_revisiones.html'
    context_object_name = 'por_revisar'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión', id=self.kwargs['pk']).order_by('-fecha')

class ContenidosApublicarView(ListView):
    model = Contenido
    template_name = 'contenido/contenido_a_publicar.html'
    context_object_name = 'revisados'

    def get_queryset(self):
        return Contenido.objects.filter(estado='A publicar').order_by('-fecha')
    
class UnContenidoApublicarView(ListView):
    model = Contenido
    template_name = 'contenido/contenido_a_publicar.html'
    context_object_name = 'revisados'

    def get_queryset(self):
        return Contenido.objects.filter(estado='A publicar', id=self.kwargs['pk']).order_by('-fecha')

@permission_required('contenido.puede_editar_aceptar')
def apublicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    if request.method == 'POST':
        nota = request.POST.get('nota')
        contenido.nota = nota
        # Cambiar el estado del contenido a "A publicar"
        contenido.estado = 'A publicar'
        contenido.save(user=request.user)
        context = {
                'titulo': contenido.titulo,      
            }      
        message = strip_tags(render_to_string('notificaciones/a_publicar.html', context))
        send_mail('Cambio de estado de publicacion',message,'cmsis2eq01@gmail.com',[contenido.user.email], fail_silently=False)

        # Redirigir a la lista de revisiones
        return redirect('listar_revisiones')
    
    return render(request, 'contenido/dar_nota_form.html', {'contenido': contenido, 'opcion': 'revisado'})

@permission_required('contenido.puede_publicar_rechazar')
def publicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    if request.method == 'POST':
        nota = request.POST.get('nota')
        contenido.nota = nota
        # Cambiar el estado del contenido a "Publicado"
        contenido.estado = 'Publicado'
        contenido.save(user=request.user)
        context = {
                'titulo': contenido.titulo,      
            }      
        message = strip_tags(render_to_string('notificaciones/publicado.html', context))
        send_mail('Cambio de estado de publicacion',message,'cmsis2eq01@gmail.com',[contenido.user.email], fail_silently=False)

        # Redirigir a la lista de a publicar
        return redirect('list_a_publicar')
    
    return render(request, 'contenido/dar_nota_form.html', {'contenido': contenido, 'opcion': 'publicar'})

@permission_required('contenido.puede_publicar_rechazar')
def rechazar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    if request.method == 'POST':
        nota = request.POST.get('nota')
        contenido.nota = nota
        # Cambiar el estado del contenido a "Rechazado"
        contenido.estado = 'Rechazado'
        contenido.save(user=request.user)
        context = {
            'titulo': contenido.titulo,  
            'nota': contenido.nota,    
        }      
        message = strip_tags(render_to_string('notificaciones/rechazado.html', context))
        send_mail('Cambio de estado de publicacion',message,'cmsis2eq01@gmail.com',[contenido.user.email], fail_silently=False)
        return redirect('list_a_publicar')

    return render(request, 'contenido/dar_nota_form.html', {'contenido': contenido, 'opcion': 'rechazar'})

class ContenidoBorradorListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Contenido
    permission_required = 'contenido.add_contenido'
    template_name = 'borrador/borradores_lista.html'
    context_object_name = 'contenidos_borrador'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Borrador').order_by('-fecha')

class ContenidoRechazadoListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Contenido
    permission_required = 'contenido.add_contenido'
    template_name = 'contenido/rechazados_lista.html'
    context_object_name = 'contenidos_rechazados'

    def get_queryset(self):
        # Obtener los contenidos en estado "rechazado" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Rechazado').order_by('-fecha')

def detalle_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if contenido.solo_suscriptores and not request.user.is_authenticated:
        return redirect('error403')
    
    if request.user.is_authenticated:
        user_likes_contenido = request.user.contenido_likes.filter(id=contenido.id).exists()
    else:
        user_likes_contenido = False
    
    return render(request, 'contenido/contenido_detalle.html', {'contenido': contenido, 'user_likes_contenido': user_likes_contenido})

def error403(request):
    return render(request, 'error/forbidden.html')

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
    
class EditarContenidoView(UpdateView, PermissionRequiredMixin):
    model = Contenido
    permission_required = 'contenido.change_contenido'
    form_class = ContenidoEditForm
    template_name = 'contenido/contenido_editar.html'
    success_url = reverse_lazy('listar_revisiones')

    def form_valid(self, form):
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=form.instance, image=image)

        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=form.instance, video=video)
        
        contenido = form.save(commit=False)
        contenido.save(user=self.request.user)

        return redirect(reverse_lazy('listar_revisiones'))
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditarBorradorView(UpdateView):
    model = Contenido
    form_class = BorradorEditForm
    template_name = 'borrador/borrador_editar.html'
    success_url = reverse_lazy('borradores_lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if  'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                form.instance.estado = 'En revisión'
                context = {'titulo': form.instance.titulo, }      
                message = strip_tags(render_to_string('notificaciones/en_revision.html', context))
                send_mail('Cambio de estado de publicacion', message, 'cmsis2eq01@gmail.com' , [form.instance.user.email]  , fail_silently=False)
            else:
                form.instance.estado = 'Publicado'
                context = {'titulo': form.instance.titulo, }      
                message = strip_tags(render_to_string('notificaciones/publicado.html', context))
                send_mail('Cambio de estado de publicacion', message, 'cmsis2eq01@gmail.com' , [form.instance.user.email]  , fail_silently=False)
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'

        contenido = form.save(commit=False)
        contenido.save(user=self.request.user)

        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=contenido, image=image)
        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=contenido, video=video)
        return redirect(reverse_lazy('borradores_lista'))
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditarRechazadoView(UpdateView):
    model = Contenido
    form_class = RechazadoEditForm
    template_name = 'contenido/rechazado_editar.html'
    success_url = reverse_lazy('rechazados_lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if  'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                form.instance.estado = 'En revisión'
            else:
                form.instance.estado = 'Publicado'
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'
        contenido = form.save(commit=False)
        contenido.save(user=self.request.user)

        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=contenido, image=image)
        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=contenido, video=video)
        return redirect(reverse_lazy('rechazados_lista'))
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

def detalle_autor(request, pk):
    # Obtiene el usuario (autor) por su clave primaria (pk)
    autor = get_object_or_404(User, pk=pk)

    # Obtiene los contenidos relacionados al autor
    contenidos = Contenido.objects.filter(user=autor,estado='Publicado').order_by('-fecha')

    # Renderiza el template para mostrar los detalles del autor y sus contenidos
    return render(request, 'autor/contenidos_autor.html', {'autor': autor, 'contenidos': contenidos})

@permission_required('contenido.ver_kanban')
def kanban_view(request):
    contexto={'contenidos': Contenido.objects.filter(user=request.user).order_by('-fecha')}
    return render(request, 'kanban.html', contexto)

@permission_required('contenido.ver_todos_kanban')
def all_kanban_view(request):
    contexto={'contenidos': Contenido.objects.all().order_by('-fecha')}
    return render(request, 'kanban.html', contexto)

def delete_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    if request.user == image.contenido.user:
        content_pk = image.contenido.pk
        estado = image.contenido.estado 
        image.delete()
        print(estado)
        if estado == 'Borrador':
            edit_url = 'editar-borrador'
        elif estado == 'Publicado' or 'En revisión':
            edit_url = 'editar-contenido'
        else:
            pass
        return redirect(edit_url, pk=content_pk)
    
def delete_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.user == video.contenido.user:
        content_pk = video.contenido.pk
        estado = video.contenido.estado
        video.delete()
        if estado == 'Borrador':
            edit_url = 'editar-borrador'
        elif estado == 'Publicado' or 'En revisión':
            edit_url = 'editar-contenido'
        else:
            pass
        return redirect(edit_url, pk=content_pk)

class ContenidoVersionListView(LoginRequiredMixin, ListView):
    model = VersionContenido
    template_name = 'version/version_lista.html'
    context_object_name = 'version_contenidos'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return VersionContenido.objects.all().order_by('-contenido_id', 'version')
    


def editar_version(request, version_id):
    version = get_object_or_404(VersionContenido, pk=version_id)
    
    if request.method == 'POST':
        form = VersionContenidoEditForm(request.POST, instance=version, user_request=request.user)
        if form.is_valid():
            nueva_version = form.save(commit=False)

        if version.contenido.estado == 'Borrador':
            contenido = version.contenido
            contenido.titulo = nueva_version.titulo
            contenido.resumen = nueva_version.resumen
            contenido.descripcion = nueva_version.descripcion
            contenido.categoria = nueva_version.categoria
            contenido.estado = nueva_version.estado
            contenido.nota = nueva_version.nota
            contenido.save()

            return redirect(reverse_lazy('contenido-version'))  # Redirigir a la lista de versiones
    else:
        form = VersionContenidoEditForm(instance=version, user_request=request.user)
    
    return render(request, 'version/version_editar.html', {'form': form, 'version': version})