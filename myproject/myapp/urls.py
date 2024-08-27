from django.urls import path
from .views import RegisterView, LoginView, SaveRecipeView,UserSavedRecipesView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user/<str:username>/save-recipe/', SaveRecipeView.as_view(), name='save-recipe'),
    path('user/<int:user_id>/saved-recipes/', UserSavedRecipesView.as_view(), name='user-saved-recipes')
]
