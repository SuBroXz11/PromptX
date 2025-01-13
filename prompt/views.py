from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PromptSerializer
from rest_framework import status
from .models import Prompt
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

class PromptView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        """
        Override this method to allow unrestricted access for GET
        and enforce authentication for POST and DELETE.
        """
        if self.request.method == 'GET':
            return [AllowAny()]  # Allow anyone to access GET requests
        return [IsAuthenticated()]  
    
    def get(self, request):
        try:
            prompts = Prompt.objects.all()  # Fetch all prompts
            if request.GET.get('search'):
                search = request.GET.get('search')
                prompts = prompts.filter(Q(title__icontains=search) | Q(prompt_text__icontains=search))
            serializer = PromptSerializer(prompts, many=True)
            return Response({
                'message': 'Prompts fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = PromptSerializer(data=request.data, context={'request': request})  

            if not serializer.is_valid():
                return Response({
                    'message': 'Invalid data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'message': 'Prompt created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def delete(self, request, pk=None):
        try:
            prompt = Prompt.objects.filter(user=request.user, id=pk).first()

            if not prompt:
                return Response({
                    'message': 'Prompt not found or not authorized to delete'
                }, status=status.HTTP_404_NOT_FOUND)

            # Delete the associated image file if it exists
            if prompt.main_image and prompt.main_image.storage.exists(prompt.main_image.name):
                prompt.main_image.storage.delete(prompt.main_image.name)

            prompt.delete()

            return Response({
                'message': 'Prompt deleted successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
