""" Various utility class and functions """

import typing as t
import re

_HEX_RGB_RE = re.compile(
    r"#(?P<red>[0-9a-fA-F]{2})(?P<green>[0-9a-fA-F]{2})(?P<blue>[0-9a-fA-F]{2})"
)


class RGBColor(t.NamedTuple):
    """8-bit RGB color"""

    red: int
    green: int
    blue: int

    def as_hex(self) -> str:
        """Hex-formatted RGB color"""
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"

    def __str__(self) -> str:
        return self.as_hex()

    def to_uint24(self) -> int:
        """Represent as a 24-bit unsigned integer, 0xRRGGBB"""
        return (
            ((self.red & 0xFF) << 16) + ((self.green & 0xFF) << 8) + (self.blue & 0xFF)
        )

    @classmethod
    def from_uint24(cls, data: int):
        """Load from a :to_uint24: representation"""
        red = (data >> 16) & 0xFF
        green = (data >> 8) & 0xFF
        blue = data & 0xFF
        return cls(red=red, green=green, blue=blue)

    @classmethod
    def from_hex(cls, hexcolor: str) -> "RGBColor":
        """Load from a hex-formatted color."""
        # This could be simply implemented as cls.from_uint24(int(hexcolor[1:])), but
        # error handling is less trivial this way -- here, the regex either matches or
        # does not.
        match = _HEX_RGB_RE.fullmatch(hexcolor)
        if match:
            r, g, b = map(lambda x: int(x, 16), match.groups())
            return cls(r, g, b)
        raise ValueError(f"Not a valid hex-formatted RGB color: {hexcolor}")
