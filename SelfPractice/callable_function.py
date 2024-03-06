from __future__ import annotations

from typing import Callable

ConversionFunc = Callable[[float], None]


def convert(input_value: float, conversion: ConversionFunc) -> None:
    conversion(input_value)


def inches_to_cm(input_value: float) -> None:
    """Print input value transformed from inch to cm."""
    output_value = input_value * 2.54
    print(f"{input_value} inches becomes {output_value:.4f} centimeters.")


def miles_to_km(input_value: float):
    """Print input value transformed from miles to km."""
    output_value = input_value * 1.609
    print(f"{input_value} miles becomes {output_value:.4f} kilometers.")


def pound_to_kg(input_value: float):
    """Print input value transformed pounds to kg."""
    output_value = input_value / 2.205
    print(f"{input_value} pounds becomes {output_value:.4f} kilograms.")


def main() -> None:
    input_value = 40

    convert(input_value, inches_to_cm)
    convert(input_value, miles_to_km)
    convert(input_value, pound_to_kg)


if __name__ == "__main__":
    main()
