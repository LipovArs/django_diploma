from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.generic import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import CreateUserForm, LoginUserForm, BecomeAssigner

from .models import Task
from django.contrib.auth.models import User

from operator import add, sub
from rest_framework.authtoken.models import Token

# Create your views here.
#@login_required(login_url='board:registration')
def home_view(request):

    current_user = request.user
    new_tasks = Task.objects.filter(status='1')
    progres_tasks = Task.objects.filter(status='2')
    qa_tasks = Task.objects.filter(status='3')
    ready_tasks = Task.objects.filter(status='4')
    done_tasks = Task.objects.filter(status='5')
    users = User.objects.filter(is_superuser=False)
    context = {
            'current_user': current_user,
            'new_tasks': new_tasks,
            'progres_tasks': progres_tasks,
            'qa_tasks': qa_tasks,
            'ready_tasks': ready_tasks,
            'done_tasks': done_tasks,
            'users': users,
    }

    return render(request, 'board/home.html', context=context)


def registration_view(request):

    form_create = CreateUserForm()
    form_login = LoginUserForm()

    if request.method == 'POST':
        if 'register_input' in request.POST:
            form_create = CreateUserForm(request.POST)

            if form_create.is_valid():
                form_create.save()
                return redirect('board:home')
        elif 'login_input' in request.POST:
            form = LoginUserForm(request, data=request.POST)

            if form.is_valid():

                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:

                    auth.login(request, user)

                    Token.objects.get_or_create(user=user)

                    return redirect('board:home')
                
    
    return render(request, 'board/registration.html', context={'form_create': form_create, 'form_login': form_login})


def logout_view(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    auth.logout(request)
    return redirect('board:home')


class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'description']
    success_url = reverse_lazy('board:home')

    def form_valid(self, form): 
        form.instance.status = '1'
        form.instance.creator = self.request.user
        form.instance.assigner = None
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    
    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().creator != self.request.user) and not self.request.user.is_superuser:
            return redirect('board:home')
        return super(TaskUpdateView, self).dispatch(request, *args, **kwargs)

    model = Task
    fields = ['name', 'description']
    success_url = reverse_lazy('board:home')


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper


@superuser_required()
class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('board:home')


    #def get(self, request, *args, **kwargs):
    #    return self.post(request, *args, **kwargs)


def change_satus_help(task, operator):
    task.status = operator(int(task.status), 1)
    task.assigner = None
    task.save()


#@login_required(login_url='board:registration')
def change_status(request, pk, direction):

    if Task.objects.filter(id=pk).exists():
        task = Task.objects.get(id=pk)
        if request.user.is_superuser:
            if direction == 'right' and int(task.status) == 4:
                change_satus_help(task, add)
            elif direction == 'left'and int(task.status) == 5:
                change_satus_help(task, sub)
        elif (task.assigner and task.assigner == request.user):
            if direction == 'right' and int(task.status) < 4:
                change_satus_help(task, add)
            elif direction == 'left'and int(task.status) > 1:
                change_satus_help(task, sub)
    
    return redirect('board:home')


#@login_required(login_url='board:registration')
def become_assigner(request, pk):

    if Task.objects.filter(id=pk).exists():
        task = Task.objects.get(id=pk)
        if task.creator == request.user:
            task.assigner = request.user
            task.save()

    return redirect('board:home')

@user_passes_test(lambda u: u.is_superuser)
def appoint_assigner(request, pk):

    selected_user_id = request.POST['assigner_select']
    if Task.objects.filter(id=pk).exists():
        task = Task.objects.get(id=pk)
        if request.user.is_superuser:
            if User.objects.filter(id=selected_user_id).exists():
                task.assigner = User.objects.get(id=selected_user_id)
                task.save()

    return redirect('board:home')


def check_status(request, status_id):

    if Task.objects.filter(status=status_id).exists():
        return render(request, 'board/check_status.html', context={'tasks': Task.objects.filter(status=status_id)})

    return redirect('board:home')
