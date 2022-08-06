from django.shortcuts import render, redirect
from .models import Finch, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.http import HttpResponse

# Add the Cat class & list and view function below the imports
def finches_index(request):
  finches = Finch.objects.filter(user=request.user)
  return render(request, 'finches/index.html', { 'finches': finches })


def home(request):
  return HttpResponse('<h1>Welcome to the website</h1>')

def about(request):
  return render(request, 'about.html')


class Home(LoginView):
  template_name = 'home.html'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('cats_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

def finches_detail(request, finch_id):
  @login_required
  def cats_index(request):
    finch = Finch.objects.get(id=finch_id)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
    'finch': finch, 'feeding_form': feeding_form, 'toys': toys_finch_doesnt_have
  })


def add_feeding(request, finch_id):
  @login_required
  def cats_index(request):
    form = FeedingForm(request.POST)
    if form.is_valid():
      new_feeding = form.save(commit=False)
      new_feeding.finch_id = finch_id
      new_feeding.save()
      return redirect('finches_detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
  @login_required
  def cats_index(request):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('cats_detail', cat_id=finch_id)

class FinchCreate(CreateView, LoginRequiredMixin):
  fields = ['name', 'breed', 'description', 'age']
  def form_valid(self, form):
    form.instance.user = self.request.user  
    return super().form_valid(form)

class FinchUpdate(UpdateView, LoginRequiredMixin):
  model = Finch
  fields = ['breed', 'description', 'age']

class FinchDelete(DeleteView, LoginRequiredMixin):
  model = Finch
  success_url = '/finches/'

class ToyCreate(CreateView, LoginRequiredMixin):
  model = Toy
  fields = '__all__'

class ToyList(ListView, LoginRequiredMixin):
  model = Toy

class ToyDetail(DetailView, LoginRequiredMixin):
  model = Toy

class ToyUpdate(UpdateView, LoginRequiredMixin):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView, LoginRequiredMixin):
  model = Toy
  success_url = '/toys/'