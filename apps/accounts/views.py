from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.services.auth_service import AuthService


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = AuthService.parse_body(request)
            user = AuthService.register_user(payload)
            return JsonResponse(
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'message': 'Usuario registrado correctamente.',
                },
                status=201,
            )
        except ValidationError as exc:
            return JsonResponse({'error': str(exc)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = AuthService.parse_body(request)
            user = AuthService.login_user(request, payload)
            return JsonResponse({'message': 'Inicio de sesión exitoso.', 'user_id': user.id}, status=200)
        except ValidationError as exc:
            return JsonResponse({'error': str(exc)}, status=400)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user = request.user
        return JsonResponse(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'company_name': user.company_name,
                'phone_number': user.phone_number,
            }
        )
