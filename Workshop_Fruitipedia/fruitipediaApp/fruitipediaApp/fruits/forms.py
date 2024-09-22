from django import forms
from fruitipediaApp.fruits.models import Category, Fruit


class CategoryBaseForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Category Name'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''


class CategoryAddForm(CategoryBaseForm):
    pass


class FruitBaseForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Fruit Name'}),
            'image_url': forms.TextInput(attrs={'placeholder': 'Fruit Image URL'}),
            'description': forms.TextInput(attrs={'placeholder': 'Fruit Description'}),
            'nutrition': forms.TextInput(attrs={'placeholder': 'Nutrition Info'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''


class FruitAddForm(FruitBaseForm):
    pass


class EditFruitForm(FruitBaseForm):
    pass


class DeleteFruitForm(FruitBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.disabled = True
