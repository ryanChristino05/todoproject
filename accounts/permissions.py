from rest_framework import permissions

class IsAuthenticatedOrSession(permissions.BasePermission):
    """
    Permission that allows access if:
    1. User is authenticated via REST Framework
    2. User has an active session (Django session middleware)
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated via REST Framework
        if request.user and request.user.is_authenticated:
            return True
        
        # Check if there's a valid session (Django session)
        # If user_id is in session, they're authenticated
        if hasattr(request, 'session') and request.session.get('_auth_user_id'):
            return True
        
        # If none of the above, deny
        return False
