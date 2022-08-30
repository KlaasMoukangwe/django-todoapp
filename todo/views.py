from contextlib import _RedirectStream
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .models import Todo

# Create your views here.


class FirstLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todolist')

class FirstRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todolist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(FirstRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return _RedirectStream('todolist')
        return super(FirstRegisterView, self).get(*args, **kwargs)


class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todolist.html'
    context_object_name = 'todos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = context['todos'].filter(user=self.request.user)
        return context
    

class TodoDetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = 'todo'
    success_url = reverse_lazy('todolist')

class TodoCreate(LoginRequiredMixin, CreateView):
    template_name = 'todo_form.html'
    model = Todo
    fields = ['title', 'complete']
    success_url = reverse_lazy('todolist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TodoCreate, self).form_valid(form)


class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    fields = ['title', 'complete']
    success_url = reverse_lazy('todolist')
    template_name = 'todo_confirm_delete.html'
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'complete']
    success_url = reverse_lazy('todolist')
    template_name = 'update_form.html'
