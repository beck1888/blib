"""
convert.py

Unit conversion utilities for distance, weight, and time between
metric and imperial systems. Includes a utility for rounding values.

Functions:
    meters_to_feet(meters): Convert meters to feet.
    feet_to_meters(feet): Convert feet to meters.
    kilometers_to_miles(km): Convert kilometers to miles.
    miles_to_kilometers(miles): Convert miles to kilometers.
    centimeters_to_inches(cm): Convert centimeters to inches.
    inches_to_centimeters(inches): Convert inches to centimeters.
    kilograms_to_pounds(kg): Convert kilograms to pounds.
    pounds_to_kilograms(lb): Convert pounds to kilograms.
    grams_to_ounces(g): Convert grams to ounces.
    ounces_to_grams(oz): Convert ounces to grams.
    seconds_to_minutes(seconds): Convert seconds to minutes.
    minutes_to_seconds(minutes): Convert minutes to seconds.
    minutes_to_hours(minutes): Convert minutes to hours.
    hours_to_minutes(hours): Convert hours to minutes.
    hours_to_days(hours): Convert hours to days.
    days_to_hours(days): Convert days to hours.
    round_to(value, decimals): Round a value to a specified number of decimal places.
"""

# Distance conversions
def meters_to_feet(meters: float) -> float:
    """
    Convert meters to feet.

    Args:
        meters (float): Distance in meters.

    Returns:
        float: Distance in feet.
    """
    return meters * 3.28084

def feet_to_meters(feet: float) -> float:
    """
    Convert feet to meters.

    Args:
        feet (float): Distance in feet.

    Returns:
        float: Distance in meters.
    """
    return feet / 3.28084

def kilometers_to_miles(km: float) -> float:
    """
    Convert kilometers to miles.

    Args:
        km (float): Distance in kilometers.

    Returns:
        float: Distance in miles.
    """
    return km * 0.621371

def miles_to_kilometers(miles: float) -> float:
    """
    Convert miles to kilometers.

    Args:
        miles (float): Distance in miles.

    Returns:
        float: Distance in kilometers.
    """
    return miles / 0.621371

def centimeters_to_inches(cm: float) -> float:
    """
    Convert centimeters to inches.

    Args:
        cm (float): Distance in centimeters.

    Returns:
        float: Distance in inches.
    """
    return cm * 0.393701

def inches_to_centimeters(inches: float) -> float:
    """
    Convert inches to centimeters.

    Args:
        inches (float): Distance in inches.

    Returns:
        float: Distance in centimeters.
    """
    return inches / 0.393701

# Weight conversions
def kilograms_to_pounds(kg: float) -> float:
    """
    Convert kilograms to pounds.

    Args:
        kg (float): Weight in kilograms.

    Returns:
        float: Weight in pounds.
    """
    return kg * 2.20462

def pounds_to_kilograms(lb: float) -> float:
    """
    Convert pounds to kilograms.

    Args:
        lb (float): Weight in pounds.

    Returns:
        float: Weight in kilograms.
    """
    return lb / 2.20462

def grams_to_ounces(g: float) -> float:
    """
    Convert grams to ounces.

    Args:
        g (float): Weight in grams.

    Returns:
        float: Weight in ounces.
    """
    return g * 0.035274

def ounces_to_grams(oz: float) -> float:
    """
    Convert ounces to grams.

    Args:
        oz (float): Weight in ounces.

    Returns:
        float: Weight in grams.
    """
    return oz / 0.035274

# Time conversions
def seconds_to_minutes(seconds: float) -> float:
    """
    Convert seconds to minutes.

    Args:
        seconds (float): Time in seconds.

    Returns:
        float: Time in minutes.
    """
    return seconds / 60

def minutes_to_seconds(minutes: float) -> float:
    """
    Convert minutes to seconds.

    Args:
        minutes (float): Time in minutes.

    Returns:
        float: Time in seconds.
    """
    return minutes * 60

def minutes_to_hours(minutes: float) -> float:
    """
    Convert minutes to hours.

    Args:
        minutes (float): Time in minutes.

    Returns:
        float: Time in hours.
    """
    return minutes / 60

def hours_to_minutes(hours: float) -> float:
    """
    Convert hours to minutes.

    Args:
        hours (float): Time in hours.

    Returns:
        float: Time in minutes.
    """
    return hours * 60

def hours_to_days(hours: float) -> float:
    """
    Convert hours to days.

    Args:
        hours (float): Time in hours.

    Returns:
        float: Time in days.
    """
    return hours / 24

def days_to_hours(days: float) -> float:
    """
    Convert days to hours.

    Args:
        days (float): Time in days.

    Returns:
        float: Time in hours.
    """
    return days * 24

# Utility for rounding
def round_to(value: float, decimals: int = 2) -> float:
    """
    Round a value to a specified number of decimal places.

    Args:
        value (float): The value to round.
        decimals (int, optional): The number of decimal places. Defaults to 2.

    Returns:
        float: The rounded value.
    """
    return round(value, decimals)