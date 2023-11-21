"""This module tests the functions in the handlers module. 
"""

import unittest
from v1.messages.views.handlers import is_valid_e164, send_sms
from parameterized import parameterized

class HandlerTest(unittest.TestCase):
    """This tests the functions in handler."""
    def setUp(self):
        """Initializes external dependencies"""
        pass
    @parameterized.expand([
        ("+2341234567867", True),
        ("08123456786", False), 
        (8123456786, False),
		("Dennis", False), 
    ]) 
    def test_is_valid_e164(self, phone_number, expected_result):
        result = is_valid_e164(phone_number)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
    	({"to": ["2"], "message": "hey there"}, ["2"], ["NotDelivered"], ["https://denniscode.tech"]),
    	({"to": ["+5018105654558"], "message": "hey there"}, ["+5018105654558"], ["DeliveredToNetwork"], ["https://denniscode.tech"]),
    	({"to": ["2", "+5018105654558"], "message": "hey there"},  ["2", "+5018105654558"], ["NotDelivered", "DeliveredToNetwork"], ["https://denniscode.tech", "https://denniscode.tech"]),
   ])
    def test_send_sms(self, pay_load, expected_to, expected_delivery_status, 
expected_sms_status_url):
        result = send_sms(pay_load)
        is_dict = isinstance(result, dict)
        self.assertEqual(True, is_dict)
        has_messages_key = result.get("messages", None)
        self.assertNotEqual(None, has_messages_key)
        dict_item = result["messages"]
        is_list = isinstance(dict_item, list)
        self.assertEqual(True, is_list)
        all_list_item_is_dict = all(isinstance(item, dict) for item in dict_item)
        self.assertEqual(True, all_list_item_is_dict)
        dict_has_four_keys = all(len(item) == 4 for item in dict_item)
        self.assertEqual(True, dict_has_four_keys)
        for i in range(len(dict_item)):
            dict_item_to = dict_item[i]["to"]
            self.assertEqual(dict_item_to, expected_to[i])

            dict_item_delivery_status = dict_item[i]["deliveryStatus"]
            self.assertEqual(dict_item_delivery_status, expected_delivery_status[i])

            dict_item_url = dict_item[i]["smsStatusURL"]
            url_starts_with_expected_sms_status_url= dict_item_url.startswith(expected_sms_status_url[i])
            self.assertEqual(True, url_starts_with_expected_sms_status_url)
