# -*- coding: utf-8 -*-
"""
Views for customerdataapi.
"""
from __future__ import absolute_import, unicode_literals
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response


from customerdataapi.models import CustomerData
from customerdataapi.serializers import CustomerDataSerializer
from paypal.standard.forms import PayPalPaymentsForm

#importing modules for paypal

from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt


#Going to import http reponse and json response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from rest_framework.parsers import JSONParser
from .models import CustomerData
from .serializers import  CustomerDataSerializer


#Sandbox imports
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
import sys
from django.views.generic import TemplateView


import json
from django.db import transaction

from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


class CustomerDataViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving CustomerData.
    """

    #Methods: list, create, retrieve, update, patial_update, destroy

    queryset = CustomerData.objects.all()
    serializer_class = CustomerDataSerializer
    permission_classes = (permissions.AllowAny,)


class PayPalClient:
    def __init__(self):
        self.client_id = "AdqJbdXIlVZsTzaLP8DXBaYaMZOm4HFsIHnFv8z3c_ppMuNpjDhCyqdrR829PbMMep6L8gJ_1iy_LpKy"
        self.client_secret = "EBdq-Z-QRCxbXSkOUASMBvSoMTH9JpKT-sRJ_DS27arFn4PkogdyKHak9oI2owrwuSo6mKfpuXg3OaBi"

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result;
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result;

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)  

class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print ('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
    #   print ("\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
    #     response.result.payer.name.given_name + " " + response.result.payer.name.surname,
    #     response.result.payer.phone.phone_number.national_number)
    return response


# """This driver function invokes the capture order function.
# Replace Order ID value with the approved order ID. """
# if __name__ == "__main__":
#   order_id = 'REPLACE-WITH-APPORVED-ORDER-ID'
#   CaptureOrder().capture_order(order_id, debug=True)

#Paypal view toget order
class GetOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """You can use this function to retrieve an order by passing order ID as an argument"""   
  def get_order(self, order_id):
    """Method to get order"""
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
    print ('Status Code: ', response.status_code)
    print ('Status: ', response.result.status)
    print ('Order ID: ', response.result.id)
    print ('Intent: ', response.result.intent)
    print ('Links:')
    for link in response.result.links:
      print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    print ('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,response.result.purchase_units[0].amount.value))

# """This driver function invokes the get_order function with
#    order ID to retrieve sample order details. """
# if __name__ == '__main__':
#   GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')  

#Reading the json file and extracting the information.
a_file = open("/home/kike/Documents/test/edunext-challenge-V4/edunext-challenge/Codecamp/001_challenge_stack/customerdataapi/initial_data.json", "r")
json_object = json.load(a_file)
for line in json_object:
    print(json_object[7]['fields']['data'])
   

def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "19.95",
        "item_name": "Subscription",
        "invoice": "unique-invoice-id",
        'payment_date': timezone.now().strftime('%H:%M:%S %b %d, %Y') + ' CET',
        "notify_url": "http://0.0.0.0:8010/paypal" + reverse('paypal-ipn'),
        "return_url": "http://0.0.0.0:8010/paypal/accepted",
        "cancel_return": "http://0.0.0.0:8010/paypal/cancel",

    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render_to_response("customerdataapi/pay.html", context)

    print(context)