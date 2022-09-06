from backend import models as backend_models
from .view_utils import TokenAuthMixin, APIView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.db.models.query import QuerySet
from django.http import JsonResponse


class LoyaltyCardAuthenticatedMixin(TokenAuthMixin):
    """Restricts the queryset to the LoyaltyCards owned by the authenticated user"""

    def get_queryset(self) -> QuerySet:
        return backend_models.LoyaltyCard.objects.filter(owner=self.auth_token.user)


class CardsGet(LoyaltyCardAuthenticatedMixin, MultipleObjectMixin, APIView):
    """Get the list of cards of this user, mapped to their revision ID"""

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> JsonResponse:
        cards = self.get_queryset()
        data = {str(card.uuid): card.revision_id for card in cards}
        return JsonResponse(data)


class CardGet(LoyaltyCardAuthenticatedMixin, SingleObjectMixin, APIView):
    """Get the details of a single card"""

    pk_url_kwarg = "uuid"

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        card = self.get_object()
        data = {
            "uuid": str(card.uuid),
            "store": card.store,
            "note": card.note,
            "expiracy": card.expiracy,
            "balance": card.balance,
            "balance_currency": card.balance_currency,
            "card_id": card.card_id,
            "barcode_id": card.barcode_id_raw,
            "header_color": card.header_color.as_hex(),
            "star_status": card.star_status,
            "archive_status": card.archive_status,
            "last_used": card.last_used,
            "zoom_level": card.zoom_level,
            "revision_id": card.revision_id,
        }
        return JsonResponse(data)
