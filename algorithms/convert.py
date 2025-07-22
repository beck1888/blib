"""
conversions.py

Unit conversion utilities for distance, weight, and time between
metric and imperial systems.
"""

# Distance conversions
def meters_to_feet(meters: float) -> float:
    return meters * 3.28084

def feet_to_meters(feet: float) -> float:
    return feet / 3.28084

def kilometers_to_miles(km: float) -> float:
    return km * 0.621371

def miles_to_kilometers(miles: float) -> float:
    return miles / 0.621371

def centimeters_to_inches(cm: float) -> float:
    return cm * 0.393701

def inches_to_centimeters(inches: float) -> float:
    return inches / 0.393701

# Weight conversions
def kilograms_to_pounds(kg: float) -> float:
    return kg * 2.20462

def pounds_to_kilograms(lb: float) -> float:
    return lb / 2.20462

def grams_to_ounces(g: float) -> float:
    return g * 0.035274

def ounces_to_grams(oz: float) -> float:
    return oz / 0.035274

# Time conversions
def seconds_to_minutes(seconds: float) -> float:
    return seconds / 60

def minutes_to_seconds(minutes: float) -> float:
    return minutes * 60

def minutes_to_hours(minutes: float) -> float:
    return minutes / 60

def hours_to_minutes(hours: float) -> float:
    return hours * 60

def hours_to_days(hours: float) -> float:
    return hours / 24

def days_to_hours(days: float) -> float:
    return days * 24

# Utility for rounding
def round_to(value: float, decimals: int = 2) -> float:
    return round(value, decimals)