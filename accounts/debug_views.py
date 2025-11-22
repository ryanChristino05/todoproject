"""Debug views to test session and authentication"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods

@api_view(['GET'])
def debug_session(request):
    """Debug endpoint to check session state"""
    return Response({
        'session_key': request.session.session_key,
        'session_data': dict(request.session),
        '_auth_user_id': request.session.get('_auth_user_id', 'NOT FOUND'),
        'user': str(request.user),
        'user_id': request.user.id if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated,
        'cookies': dict(request.COOKIES),
    })
