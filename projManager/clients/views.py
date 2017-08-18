from django.contrib.auth.models import User

from django.shortcuts import render
from django.shortcuts import redirect

from clients.forms import LoginUserForm
from clients.forms import CreateUserForm
from clients.forms import EditUserForm
from clients.forms import EditPasswordForm

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
"""
Class
"""

class ShowClass(DetailView): # Vista publica, cada persona puede entrar a perfiles.
    model = User
    template_name = 'client/show.html'
    slug_field = 'username' # Que campo de la base de datos
    slug_url_kwarg = 'username_url' #Que de la url
    
#def show(request):
#    return HttpResponse("Hola desde el cliente")

#def login(request):
#    nombre = 'Juan Manuel'
#    edad = 34
#    context = { 'nombre' : nombre, 'edad' : edad  }
#    return render(request, 'login.html', context)

class LoginClass(View):
    form = LoginUserForm()
    message = None
    template = 'client/login.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('client:dashboard')
        return render(request, self.template, self.get_context())
    
    def post(self, request, *args, **kwargs):
        
        username_post = request.POST['username']
        password_post = request.POST['password']
        
        user = authenticate (username = username_post, password = password_post)
        if user is not None:
            login_django(request, user)
            return redirect('client:dashboard')
        else:
            self.message = "Username o password incorrecto"
        return render(request, self.template, self.get_context())
    
    def get_context(self):
        return {'form': self.form, 'message':self.message}
    
class DashboardClass(LoginRequiredMixin, View): #Mixin porque el usuario debe estar autenticado
    login_url = 'client:login'
    
    def get(self, request, *args, **kwargs): #Heredada de View
        return render( request, 'client/dashboard.html', {})

   
class CreateClass(CreateView):
    success_url = reverse_lazy('client:login')
    template_name = 'client/create.html'
    model = User
    form_class = CreateUserForm
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.set_password ( self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
class EditClass(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    login_url = 'client:login'
    model = User
    template_name = 'client/edit.html'
    success_url = reverse_lazy('client:edit')
    form_class = EditUserForm
    success_message = "Tu usuario ha sido actualizado"
    
    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EditClass, self).form_valid(request)
    
    def get_object(self, queryset = None):
        return self.request.user
 
    
"""
Functions
"""

@login_required( login_url = 'client:login' )       
def edit_password(request):
    
    form = EditPasswordForm(request.POST or None)
    context = {'form' : form}
    if request.method == 'POST':
        if form.is_valid():
            current_password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            if authenticate(username = request.user.username, password = current_password):
                request.user.set_password(new_password)
                request.user.save()
                
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password actualizado.')
            else:
                messages.error(request, 'No es posible actualizar el password.')
    context = {'form' : form}
    return render(request, 'client/edit_password.html', context)

@login_required( login_url = 'client:login' )
def logout(request):
    logout_django(request)
    return redirect('client:login')

#def login(request):
#    if request.user.is_authenticated():
#        return redirect('client:dashboard')
#    message = None
#    if request.method == 'POST': # Nos estan enviando el formulario
#        username_post = request.POST['username']
#        password_post = request.POST['password']
#        
#        user = authenticate (username = username_post, password = password_post)
#        if user is not None:
#            login_django(request, user)
#            return redirect('client:dashboard')
#        else:
#            message = "Username o password incorrecto"
#        
#    form = LoginForm()
#    context = {
#        'form' : form,
#        'message' : message
#        
#    }
#    return render(request, 'login.html', context)

#@login_required( login_url = 'client:login' ) # Si el usuario esta autenticado entra
#def dashboard(request):
#    return render( request, 'dashboard.html', {})

#def create(request):
#    form = CreateUserForm(request.POST or None)
#    if request.method == 'POST':
#        if form.is_valid():
#            user = form.save( commit = False )
#            user.set_password( user.password )
#            user.save()
#            return redirect('client:login')
#    context = {
#        'form' : form
#    }
#    return render( request, 'create.html', context)
    