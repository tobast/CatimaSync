""" Various utility class and functions """

import typing as t


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
