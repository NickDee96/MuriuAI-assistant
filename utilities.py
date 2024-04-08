from datetime import datetime
import geocoder

def get_formatted_date_time() -> str:
    """
    Get the current date and time in a formatted string.

    Returns:
        str: The formatted date and time string.
    """
    # Get the current date and time
    current_date_time = datetime.now()

    # Format the date and time as "1st Jan, 2023 12:34 PM"
    formatted_date_time = current_date_time.strftime("%d %b, %Y %I:%M %p").replace(" 0", " ")

    return formatted_date_time




def get_location():
    """
    Get the current location using geocoder.
    
    Returns:
        str: The current location.
    """
    g = geocoder.ip('me')
    location = g.address
    
    return location
