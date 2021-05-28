# -*- coding: utf-8 -*-
"""
Database models for customerdataapi.
"""

from __future__ import absolute_import, unicode_literals

import collections
import uuid
import jsonfield

from django.db import models
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.db.models.signals import pre_save



class CustomerData(models.Model):
    """
    A simple model to store our customer data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # pylint: disable=invalid-name
    data = jsonfield.JSONField(blank=True, null=True, load_kwargs={'object_pairs_hook': collections.OrderedDict})

    def __unicode__(self):
        return "CustomerData with id <{}>".format(self.id)


#Signal to receive payment and update json
def update_data(sender, instance, **kwargs):
    if created == False:
        instance.data.save()
        print('payment updated!')




def show_me_the_money(sender, **kwargs):
    ipn_obj = sender

    print(ipn_obj)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != "jporrasn@unbosque.edu.co":
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "premium_plan":
            price = 19.95
        else:
            price = 'Free'

        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
            ...
    else:
        #...
        pass

valid_ipn_received.connect(show_me_the_money)
