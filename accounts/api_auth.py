from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
import json

@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    
    try:
        # Parser le JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)
        
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        # Valider que les champs sont présents
        if not email:
            return JsonResponse({"error": "L'email est requis"}, status=400)
        
        if not password:
            return JsonResponse({"error": "Le mot de passe est requis"}, status=400)
        
        # Récupérer l'utilisateur par email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "Email introuvable"}, status=400)
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            get_token(request)
            # Renvoyer les données utilisateur comme pour le register
            return JsonResponse({
                "message": "Connexion réussie",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.first_name or user.username
                }
            }, status=200)
        
        return JsonResponse({"error": "Mot de passe incorrect"}, status=400)
    
    except Exception as e:
        # Gérer toutes les autres exceptions
        return JsonResponse({"error": f"Erreur serveur: {str(e)}"}, status=500)

"""
@csrf_exempt
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        # ✅ On passe request ici
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)     # ✅ crée la session
            get_token(request)       # ✅ assure que React garde le cookie
            return JsonResponse({"message": "Connexion réussie"}, status=200)

        return JsonResponse({"error": "Identifiants invalides"}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

"""
@csrf_exempt
def api_logout(request):
    logout(request)
    return JsonResponse({"message": "Déconnecté"}, status=200)

"""
@csrf_exempt

def api_register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Ce nom d'utilisateur existe déjà"}, status=400)

        User.objects.create_user(username=username, password=password)

        return JsonResponse({"message": "Compte créé avec succès"}, status=201)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
"""
@csrf_exempt
def api_register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    
    try:
        # Parser le JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)
        
        # Récupérer les données
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        name = data.get("name", "").strip()
        
        # Valider que les champs requis sont présents
        if not email:
            return JsonResponse({"error": "L'email est requis"}, status=400)
        
        if not password:
            return JsonResponse({"error": "Le mot de passe est requis"}, status=400)
        
        # Valider la longueur du mot de passe
        if len(password) < 6:
            return JsonResponse({"error": "Le mot de passe doit contenir au moins 6 caractères"}, status=400)
        
        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Cet email est déjà utilisé"}, status=400)
        
        # Utiliser le "name" directement comme username
        # Si name est fourni, l'utiliser tel quel, sinon utiliser l'email
        if name:
            base_username = name
        else:
            # Si pas de name, utiliser la partie avant @ de l'email
            base_username = email.split("@")[0]
        
        # S'assurer que le username est unique
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
            # Protection contre les boucles infinies
            if counter > 1000:
                return JsonResponse({"error": "Impossible de générer un nom d'utilisateur unique"}, status=500)
        
        # Créer l'utilisateur
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name if name else ""
            )
        except Exception as e:
            return JsonResponse({"error": f"Erreur lors de la création du compte: {str(e)}"}, status=400)
        
        return JsonResponse({
            "message": "Compte créé avec succès",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.first_name or user.username
            }
        }, status=201)
    
    except Exception as e:
        # Gérer toutes les autres exceptions
        return JsonResponse({"error": f"Erreur serveur: {str(e)}"}, status=500)


@csrf_exempt
def api_profile(request):
    """GET: retourne les informations du user connecté.
       PATCH/PUT: met à jour `email`, `first_name`, `last_name` du user connecté.
    """
    # Vérifier l'authentification via session Django (pas DRF)
    if not request.user or not request.user.is_authenticated:
        return JsonResponse({"error": "Non authentifié"}, status=401)

    user = request.user

    if request.method == 'GET':
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "name": user.first_name or user.username
        }, status=200)

    if request.method in ('PATCH', 'PUT'):
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Données JSON invalides"}, status=400)

            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')

            # Si email est fourni, vérifier unicité
            if email and User.objects.filter(email=email).exclude(pk=user.pk).exists():
                return JsonResponse({"error": "Cet email est déjà utilisé"}, status=400)

            if email:
                user.email = email
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name

            user.save()

            return JsonResponse({
                "message": "Profil mis à jour",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "name": user.first_name or user.username
                }
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Erreur serveur: {str(e)}"}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
