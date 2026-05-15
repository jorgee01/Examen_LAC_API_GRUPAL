from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


def get_tokens_for_user(user):
    """Genera access + refresh token para un usuario."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    POST /api/auth/google/
    Body: { "token": "<google_id_token>" }
    Valida el token de Google, busca o crea el usuario,
    y devuelve tokens JWT de acceso y refresco.
    """
    token = request.data.get('token')

    if not token:
        return Response(
            {'error': 'Se requiere el token de Google.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Validar el token con Google
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')

        if not email:
            return Response(
                {'error': 'No se pudo obtener el email del token.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar o crear usuario
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        # Generar JWT tokens
        tokens = get_tokens_for_user(user)

        return Response({
            'message': 'Login exitoso',
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            **tokens
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {'error': f'Token de Google inválido: {str(e)}'},
            status=status.HTTP_401_UNAUTHORIZED
        )
