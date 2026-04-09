import json
from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpRequest

User = get_user_model()


class AuthService:
    @staticmethod
    def register_user(payload: dict[str, Any]) -> User:
        required = ['username', 'email', 'password']
        missing = [field for field in required if not payload.get(field)]
        if missing:
            raise ValidationError(f'Campos requeridos faltantes: {", ".join(missing)}')

        if User.objects.filter(username=payload['username']).exists():
            raise ValidationError('El nombre de usuario ya existe.')

        user = User.objects.create_user(
            username=payload['username'],
            email=payload['email'],
            password=payload['password'],
            first_name=payload.get('first_name', ''),
            last_name=payload.get('last_name', ''),
            company_name=payload.get('company_name', ''),
            phone_number=payload.get('phone_number', ''),
        )
        return user

    @staticmethod
    def login_user(request: HttpRequest, payload: dict[str, Any]) -> User:
        user = authenticate(
            request,
            username=payload.get('username', ''),
            password=payload.get('password', ''),
        )
        if not user:
            raise ValidationError('Credenciales inválidas.')

        login(request, user)
        return user

    @staticmethod
    def parse_body(request: HttpRequest) -> dict[str, Any]:
        if not request.body:
            return {}
        return json.loads(request.body.decode('utf-8'))
