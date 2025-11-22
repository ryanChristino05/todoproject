from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from accounts.authentication import CsrfExemptSessionAuthentication
import logging

logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]  # ← Ajoutez cette ligne

    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            email = request.data.get('email', '').strip()
            password = request.data.get('password', '').strip()
            if not email or not password:
                return Response({'error': 'Email et mot de passe requis'}, status=400)
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Email introuvable'}, status=400)
            
            user = authenticate(request, username=user.username, password=password)
            if not user:
                return Response({'error': 'Mot de passe incorrect'}, status=400)

            django_login(request, user)
            request.session.save()
            
            # Force session cycle to ensure cookies are properly set
            request.session.cycle_key()
            request.session.save()

            return Response({
                'message': 'Connexion réussie',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': user.first_name or user.username
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response({'error': f'Erreur serveur: {str(e)}'}, status=500)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        django_logout(request)
        return Response({'message': 'Déconnexion réussie'})

    @action(detail=False, methods=['post'])
    def register(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()
        name = request.data.get('name', '').strip()
        if not email or not password:
            return Response({'error': 'Email et mot de passe requis'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email déjà utilisé'}, status=400)
        
        username = email.split('@')[0]
        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        return Response({'message': 'Compte créé', 'user': {'id': user.id, 'username': user.username, 'email': user.email, 'name': user.first_name}})

    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'authenticated': False})  # ← Retourne 200 au lieu de 403
        return Response({
            'authenticated': True,
            'user': {
                'id': user.id, 
                'username': user.username, 
                'email': user.email, 
                'name': user.first_name or user.username
            }
        })