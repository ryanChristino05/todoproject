# from rest_framework.authentication import SessionAuthentication

# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     """
#     SessionAuthentication qui désactive la vérification CSRF.
#     Nécessaire pour les appels API depuis React.
#     """
#     def enforce_csrf(self, request):
#         return  # Désactive complètement la vérification CSRF

from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """SessionAuthentication qui ignore le CSRF pour dev"""
    def enforce_csrf(self, request):
        return
