from django.db import models
from django.core import validators
from django.utils.translation import gettext as _
from uuid import uuid4 as mk_uuid4

from .util import RGBColor


class BarcodeFormat(models.TextChoices):
    """Enumeration of the supported barcode formats"""

    AZTEC = "AZTEC", "Aztec"
    CODE_39 = "C39", "Code 39"
    CODE_93 = "C93", "Code 93"
    CODE_128 = "C128", "Code 128"
    CODABAR = "CODABAR", "Codabar"
    DATA_MATRIX = "DM", "Data Matrix"
    EAN_8 = "EAN8", "EAN 8"
    EAN_13 = "EAN13", "EAN 13"
    ITF = "ITF", "ITF"
    PDF_417 = "PDF417", "PDF 417"
    QR_CODE = "QRCODE", "QR Code"
    UPC_A = "UPCA", "UPC A"
    UPC_E = "UPCE", "UPC E"


class LoyaltyCard(models.Model):
    """A loyalty card"""

    uuid = models.UUIDField(primary_key=True, default=mk_uuid4, editable=False)
    store = models.CharField(_("Name"), max_length=512)
    note = models.TextField(_("Notes"))
    expiracy = models.DateField(_("Expires on"))
    balance = models.DecimalField(_("Balance"), max_digits=8, decimal_places=2)
    balance_currency = models.CharField(
        _("Balance currency"),
        max_length=3,
        help_text=_("Currency 3-letter symbol, ISO 4217"),
    )
    card_id = models.TextField(_("Card ID"))  # QR codes can be big.
    barcode_id_raw = models.TextField(
        _("Barcode ID"),
        null=True,
        blank=True,
        help_text=_("Leave blank to reuse card ID"),
    )
    barcode_type = models.CharField(
        _("Barcode type"), max_length=7, choices=BarcodeFormat.choices
    )
    header_color_raw = models.PositiveIntegerField(
        _("Header color"),
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(0xFFFFFF),
        ],
        help_text=_("RGB color, 0xRRGGBB"),
    )
    star_status = models.BooleanField(_("Starred"), default=False)
    archive_status = models.BooleanField(_("Archived"), default=False)
    last_used = models.DateTimeField(_("Last used"))
    zoom_level = models.PositiveIntegerField(_("Zoom level"))

    revision_id = models.PositiveIntegerField(
        _("Revision ID"), default=0, editable=False
    )

    def __str__(self) -> str:
        return f"<LoyaltyCard {self.store}>"

    @property
    def barcode_id(self) -> str:
        """Barcode ID of this card, based on card_id if barcode_id_raw is empty"""
        if self.barcode_id_raw:
            return self.barcode_id_raw
        return self.card_id

    @barcode_id.setter
    def barcode_id(self, val: str):
        if val == self.card_id:
            self.barcode_id_raw = None
        else:
            self.barcode_id_raw = val

    @property
    def header_color(self) -> RGBColor:
        """Header color, as a RGBColor value. Backed by header_color_raw."""
        return RGBColor.from_uint24(self.header_color_raw)

    @header_color.setter
    def header_color(self, color: RGBColor):
        self.header_color_raw = color.to_uint24()
