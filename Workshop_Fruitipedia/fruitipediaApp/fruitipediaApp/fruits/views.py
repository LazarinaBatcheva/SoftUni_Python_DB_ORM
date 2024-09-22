from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView
from fruitipediaApp.fruits.forms import CategoryAddForm, FruitAddForm, EditFruitForm, DeleteFruitForm
from fruitipediaApp.fruits.models import Fruit, Category


def index(request):
    return render(request, 'common/index.html')


class DashboardView(ListView):
    model = Fruit
    template_name = 'common/dashboard.html'
    context_object_name = 'fruits_list'


class CreateFruitView(CreateView):
    model = Fruit
    form_class = FruitAddForm
    template_name = 'fruits/create-fruit.html'
    success_url = reverse_lazy('dashboard')


class EditFruitView(UpdateView):
    model = Fruit
    form_class = EditFruitForm
    template_name = 'fruits/edit-fruit.html'
    success_url = reverse_lazy('dashboard')


class DetailsFruitView(DetailView):
    model = Fruit
    template_name = 'fruits/details-fruit.html'
    context_object_name = 'fruit'


class DeleteFruitView(DeleteView):
    model = Fruit
    form_class = DeleteFruitForm
    template_name = 'fruits/delete-fruit.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)

        return self.render_to_response(self.get_context_data(form=form, object=self.object))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return redirect(self.success_url)


class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryAddForm
    template_name = 'categories/create-category.html'
    success_url = reverse_lazy('dashboard')
