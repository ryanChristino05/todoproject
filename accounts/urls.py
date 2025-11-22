from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import AuthViewSet

app_name = "accounts"

# DRF Router for auth endpoints
router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')

urlpatterns = [
    # Classical Django pages (use views.py)
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),

    # DRF API endpoints (via router)
    # Routes will be:
    # POST   /api/accounts/api/login/
    # POST   /api/accounts/api/logout/
    # POST   /api/accounts/api/register/
    # GET    /api/accounts/api/profile/
    # PATCH  /api/accounts/api/profile/
    path('', include(router.urls)),
]

