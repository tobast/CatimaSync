import secrets
import string
from django.db import models
from django.conf import settings
from backend.models import User
from django.contrib.auth import hashers
from django.utils.translation import gettext as _

import typing as t


class AuthToken(models.Model):
    """A token to be used to authenticate against the API"""

    _ALPHABET: str = string.ascii_letters + string.digits
    _NAME_LENGTH: int = 20
    _SECRET_LENGTH: int = 40  # 240b of entropy
    _HASHED_SECRET_LENGTH: int = 128

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_name = models.CharField(
        _("Authentication token name"),
        max_length=_NAME_LENGTH,
        editable=False,
        primary_key=True,
    )
    token_secret = models.CharField(
        _("Authentication token secret"),
        max_length=_HASHED_SECRET_LENGTH,
        editable=False,
    )
    device_name = models.TextField(_("Device name"), blank=True, null=True)
    last_used = models.DateTimeField(
        _("Last used on"), blank=True, null=True, editable=False
    )

    def _set_secret(self, new_hash: str):
        self.token_secret = new_hash
        self.save(update_fields=["token_secret"])

    @classmethod
    def check_auth(cls, token_name: str, token_secret: str) -> t.Optional["AuthToken"]:
        """Retrieve the given auth token from the database, or None if the token does
        not exist"""

        try:
            token = cls.objects.get(token_name=token_name)
        except cls.DoesNotExist:
            return None

        if hashers.check_password(
            token_secret, token.token_secret, setter=token._set_secret
        ):
            return token
        return None

    @classmethod
    def create_token(
        cls,
        for_user: User,
        for_device: str,
        token_name: t.Optional[str],
        token_secret: t.Optional[str],
    ) -> "AuthToken":
        """Generate a fresh authentication token, using the provided data if any,g
        generating random data otherwise. The returned token isn't saved yet -- the
        caller must call `.save()` on it."""

        def randK(size: int) -> str:
            """Generate :size: random characters from the alphabet from CSPRNG"""
            return "".join(secrets.choice(cls._ALPHABET) for _ in range(size))

        if token_name is None:
            token_name = randK(cls._NAME_LENGTH)
        if token_secret is None:
            token_secret = randK(cls._SECRET_LENGTH)

        hashed_secret = hashers.make_password(token_secret)

        return cls(
            user=for_user,
            token_name=token_name,
            token_secret=hashed_secret,
            device_name=for_device,
            last_used=None,
        )
