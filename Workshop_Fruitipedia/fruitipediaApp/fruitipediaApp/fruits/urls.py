from django.urls import path, include
from fruitipediaApp.fruits import views


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('create-fruit/', views.CreateFruitView.as_view(), name='create_fruit'),
    path('<int:pk>/', include([
        path('edit-fruit/', views.EditFruitView.as_view(), name='edit_fruit'),
        path('details-fruit/', views.DetailsFruitView.as_view(), name='details_fruit'),
        path('delete-fruit/', views.DeleteFruitView.as_view(), name='delete_fruit'),
    ])),
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
]
