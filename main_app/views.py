from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Plant, Fertilizer
from .forms import WateringForm


class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = ['varietal', 'description', 'age']


class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants/'


@login_required
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up. Try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def plants_index(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'plants/index.html', {'plants': plants})


@login_required
def plants_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    fertilizers_plant_doesnt_have = Fertilizer.objects.exclude(
        id__in=plant.fertilizers.all().values_list('id'))
    watering_form = WateringForm()
    return render(request, 'plants/detail.html', {
        'plant': plant,
        'watering_form': watering_form,
        'fertilizers': fertilizers_plant_doesnt_have
    })


@login_required
def add_watering(request, plant_id):
    form = WateringForm(request.POST)
    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
    return redirect('detail', plant_id=plant_id)


@login_required
def assoc_fertilizer(request, plant_id, fertilizer_id):
    Plant.objects.get(id=plant_id).fertilizers.add(fertilizer_id)
    return redirect('detail', plant_id=plant_id)


@login_required
def unassoc_fertilizer(request, plant_id, fertilizer_id):
    Plant.objects.get(id=plant_id).fertilizers.remove(fertilizer_id)
    return redirect('detail', plant_id=plant_id)
