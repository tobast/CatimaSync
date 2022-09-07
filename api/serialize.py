""" Classes working on the transition of classes to and from serialized format """

from abc import ABC
import typing as t
from django.db import models
from backend import models as backend_models
from backend.util import RGBColor

BaseModel = t.TypeVar("BaseModel", bound=models.Model)
SerializedData: t.TypeAlias = dict[str, t.Any]


class BadSerializedValue(Exception):
    """Raised when trying to unserialize a bad value for this model"""


class Serializer(ABC, t.Generic[BaseModel]):
    """A base class for serializers

    For each field `foo`, a class method `serialize_foo: t.Any -> str` and
    `unserialize_foo: str -> t.Any` can be defined, and will be called upon
    serializing/unserializing of this specific field. By default, this function is the
    identity function.
    """

    # The model being serialized
    model: t.Type[BaseModel]

    # All the fields of the model to be (un)serialized
    serialized_fields: list[str] = []

    @classmethod
    def _serialize_field(cls, field: str, value: t.Any) -> str:
        method_name = "serialize_" + field
        if hasattr(cls, method_name):  # about 2x faster than getattr() and catch exn
            return getattr(cls, method_name)(value)
        return value

    @classmethod
    def _unserialize_field(cls, field: str, value: str) -> t.Any:
        method_name = "unserialize_" + field
        if hasattr(cls, method_name):  # about 2x faster than getattr() and catch exn
            return getattr(cls, method_name)(value)
        return value

    @classmethod
    def serialize(cls, entry: BaseModel) -> SerializedData:
        """Serialize the model entry to a dictionary"""
        out: SerializedData = {}
        for field in cls.serialized_fields:
            out[field] = cls._serialize_field(field, getattr(entry, field))
        return cls.serialize_post(out)

    @classmethod
    def serialize_post(cls, serialized: SerializedData) -> SerializedData:
        """Applied after `serialize`, if some adjustments are required."""
        return serialized

    @classmethod
    def unserialize_to_attrs(cls, data: SerializedData) -> SerializedData:
        """Converts serialized data to a dict of attributes, ready to be fed to the
        model"""
        if set(cls.serialized_fields) != set(data.keys()):
            extra = set(data.keys()) - set(cls.serialized_fields)
            missing = set(cls.serialized_fields) - set(data.keys())
            msgs = []
            if extra:
                msgs.append(f"got extra keys {', '.join(extra)}")
            if missing:
                msgs.append(f"got missing keys {', '.join(missing)}")
            raise BadSerializedValue(
                f"Bad keys for {cls.model.__name__}: {', '.join(msgs)}."
            )
        out_attrs = {}
        for field, val in data.items():  # Keys are matching
            out_attrs[field] = cls._unserialize_field(field, val)

        return cls.unserialize_post(out_attrs)

    @classmethod
    def unserialize_post(cls, serialized: SerializedData) -> SerializedData:
        """Applied after `unserialize_to_attrs`, if some adjustments are required."""
        return serialized

    @classmethod
    def unserialize_to_new(cls, data: SerializedData) -> BaseModel:
        """Unserialize the given dictionary to a new, unsaved model entry"""
        attrs = cls.unserialize_to_attrs(data)
        return cls.model(**attrs)


class LoyaltyCardSerializer(Serializer[backend_models.LoyaltyCard]):
    model = backend_models.LoyaltyCard
    serialized_fields = [
        "uuid",
        "store",
        "note",
        "expiracy",
        "balance",
        "balance_currency",
        "card_id",
        "barcode_id",
        "barcode_type",
        "header_color",
        "star_status",
        "archive_status",
        "last_used",
        "zoom_level",
        "revision_id",
    ]

    @classmethod
    def serialize_header_color(cls, color: RGBColor) -> str:
        return color.as_hex()

    @classmethod
    def unserialize_header_color(cls, color: str) -> RGBColor:
        return RGBColor.from_hex(color)

    @classmethod
    def serialize_post(cls, serialized: SerializedData) -> SerializedData:
        if serialized["barcode_id"] == serialized["card_id"]:
            serialized["barcode_id"] = ""
        return serialized
