""" This module defines helper functions for the SMS API messages routes."""

import re
import uuid

def is_valid_e164(phone_number):
    """
    Check if a phone number is a valid E.164 format.

    Args:
        phone_number (str): The phone number to be validated.

    Returns:
        bool: True if the phone number is valid E.164, False otherwise.

    Example:
        Example usage to check if a phone number is valid:
        >>> phone_number = "+123456789012"
        >>> result = is_valid_e164(phone_number)
        >>> print(result)
    """
    if not isinstance(phone_number, str):
    	return False
    e164_pattern = re.compile(r'^\+\d{1,3}\d{4,14}$')
    return bool(e164_pattern.match(phone_number))

def send_sms(request_data):
    """
    Send SMS messages to a list of phone numbers.

    Args:
        request_data (dict): The request data containing 'to' field with a list of phone numbers.

    Returns:
        dict: A dictionary containing information about the sent messages.

    Example:
        Example usage when sending SMS messages:
        >>> data = {"to": ["+123456789012", "+987654321098"], "message": "Hello, world!"}
        >>> result = send_sms(data)
        >>> print(result)
    """
    messages = []
    for i in request_data["to"]:
        message_id = str(uuid.uuid4())
        if is_valid_e164(i):
            message_info = {"to": i, "deliveryStatus": "DeliveredToNetwork", "messageId": message_id, "smsStatusURL": f"https://denniscode.tech/v1/messages/sms/{message_id}/status"}
        else:
             message_info = {"to": i, "deliveryStatus": "NotDelivered", "messageId": message_id, "smsStatusURL": f"https://denniscode.tech/v1/messages/sms/{message_id}/status"}
        messages.append(message_info)
    return {"messages": messages}
