from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserSerializer, SavedRecipeSerializer
from .models import SavedRecipe




def get_tokens_for_user(user):
    access = AccessToken.for_user(user)
    return {
        "access": str(access),
    }


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token = get_tokens_for_user(user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

class SaveRecipeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SavedRecipeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Recipe saved successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserSavedRecipesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.get(id=user_id)
        saved_recipes = SavedRecipe.objects.filter(user_id=user_id)
        serializer = SavedRecipeSerializer(saved_recipes, many=True)
        return Response({
            'username': user.username,
            'saved_recipes': serializer.data
        })