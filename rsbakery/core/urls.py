from django.urls import path, include
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('recipes/', RecipeListView.as_view(), name='recipes'),
    path('create-recipe/', CreateRecipeView.as_view(), name='create-recipe'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='detail'),
    path('update-recipe/<int:pk>/', RecipeUpdateView.as_view(), name='update-recipe'),
    path('delete-recipe/<int:pk>/', RecipeDeleteView.as_view(), name='delete-recipe'),
    path('add/<int:pk>/', UpdateIngredient.as_view(), name='add-ingredients'),
    path('remove/<int:recipe>/<int:ingredient>/', RemoveIngredient.as_view(), name='remove-ingredients'),
    path('recipe-collection/', RecipeCollectionListView.as_view(), name='recipe-collection-list'),
    path('recipe/<int:pk>/add-comment/', AddComment.as_view(), name='add-comment'),
    path('remove-comment/<int:pk>/', RemoveComment.as_view(), name='remove-comment'),
    path('likes/', Likes.as_view(), name='likes'),
    path('update-collections/', UpdateCollectionView.as_view(), name='update-collections'),
    path('contact/', ContactView.as_view(), name='contact-us'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),


    
]