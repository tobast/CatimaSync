""" Utility classes for API views """

from .models import AuthToken
import typing as t
from django import http
from django.views.generic.base import View

if t.TYPE_CHECKING:
    _base_view_mixin = View
else:
    _base_view_mixin = object


class TokenAuthMixin(_base_view_mixin):
    """Checks that the user provides a correct token-based auth through headers"""

    auth_token: AuthToken

    def dispatch(self, request, *args, **kwargs) -> http.response.HttpResponseBase:
        token_name = request.headers.get("x-token-username", None)
        token_secret = request.headers.get("x-token-secret", None)
        if not token_name or not token_secret:
            return http.JsonResponse(
                {
                    "reason": "No X-Token-Username or X-Token-Secret provided",
                },
                status=403,
            )

        token = AuthToken.check_auth(token_name, token_secret)
        if token is None:
            return http.JsonResponse(
                {"reason": "Token authentication failed"},
                status=403,
            )

        self.auth_token = token
        return super().dispatch(request, *args, **kwargs)


class APIView(View):
    """A View part of the API."""

    # Override to empty list by default -- prevent mistakes
    http_method_names: list[str] = []

    def http_method_not_allowed(self, request, *args, **kwargs) -> http.HttpResponse:
        """Called when a bad method is used"""
        return http.JsonResponse(
            {"reason": f"{request.method} method not allowed for this endpoint."},
            status=405,
        )
