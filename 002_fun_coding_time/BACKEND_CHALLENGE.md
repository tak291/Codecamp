eduNEXT Coding Challenge
========================

This is the challenge for the back end developer position. You only need to answer it if you want to apply for a job in python backend end development.


Situation description
=====================

As we saw on the challenge stack section, for each of our customers, we keep a configuration object stored in the database. This configuration object is something we can interact with using a REST API that exposes the JSON for all our internal services and applications.

An example of the object we store and access for each customer is:

```
{
    "SUBSCRIPTION": "basic",
    "CREATION_DATE": "2013-03-10T02:00:00Z",
    "LAST_PAYMENT_DATE": "2010-01-10T09:25:00Z",
    "theme_name": "Tropical Island",
    "ENABLED_FEATURES": {
        "CERTIFICATES_INSTRUCTOR_GENERATION": true,
        "INSTRUCTOR_BACKGROUND_TASKS": true,
        "ENABLE_COURSEWARE_SEARCH": true,
        "ENABLE_COURSE_DISCOVERY": true,
        "ENABLE_DASHBOARD_SEARCH": true,
        "ENABLE_EDXNOTES": true
    },
    "language_code": "en",
    "banner_message": "<p><span>Welcome</span> to Mr X's website</p>",
    "displayed_timezone": "America/Bogota",
    "user_profile_image": "https://i.imgur.com/LMhM8nn.jpg",
    "user_email": "barack@aol.com"
}
```

Challenge
=========


For the challenge, please imagine your next tasks is to create a new service that sits between our payment processor (PayPal) and our customer data api. You have to create a python based service that receives the IPN notification from paypal, processes it and updates the customer information on the customer API.

You can use any version of python and any framework to create your service. We are specialized in django, so Django Rest Framework (DRF) would be our weapon of choice, but feel free to use any framework as long as it is modern. List your dependencies in a file so we can recreate your working code in a test environment.

Now, the message you are expecting to receive is an Instant Payment Notification (IPN) from paypal. So, your service is expected to be listening in localhost at the port 8000 (http://localhost:8000/payments/paypal/), and you can simulate the incoming calls from paypal using something like the following cURL example:

```
curl -i \
    -X POST -d "protection_eligibility=Eligible&address_status=confirmed&payer_id=d7f73fb3-7791-4fba-8d3c-861b80a0ceab&payment_date=20%3A12%3A59+Jan+13%2C+2009+PST&payment_status=Completed&notify_version=2.6&verify_sign=AtkOfCXbDm2hu0ZELryHFjY-Vb7PAUvS6nMXgysbElEn9v-1XcmSoGtf&receiver_id=S8XGHLYDW9T3S&txn_type=express_checkout&item_name=basic&mc_currency=USD&payment_gross=19.95&shipping=0.0" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    http://localhost:8010/paypal/
```
In this example you are getting a payment for 19.9 USD, for a customer with ID `1b2f7b83-7b4d-441d-a210-afaa970e5b76`. The payment status is `Completed` so it is a valid payment and the customer is buying the `basic` subscription tier.

Your service needs to validate that the IPN has all the required information, and then proceed to create/update the user record accordingly using the customer API.

Now the situation might be that the payment_status is something different than completed, in which case, you need to set the SUBSCRIPTION field, to `free` and make sure all the ENABLED_FEATURES are set to false.

Finally, we want to know when the users change their current plans, so we can take actions to keep the business running. If the user went from `free` to `basic` or `premium`, or from `basic` to `premium`, it means they are upgrading their account, and we need to add a or updated a key with the name `UPGRADE_DATE` with the current datetime. If the user did the opposite, downgrading from `premium` to `basic` or to `free`, we need to add or update a key called `DOWNGRADE_DATE` with the current datetime.

In the provided example, since the customer already exists, you only need to set the following fields of the customer object:

```
    "SUBSCRIPTION": "premium",
    "LAST_PAYMENT_DATE": "2018-01-10T09:25:00Z"   (current datetime)
```

You can use the provided cURL example and modify it however you need to simulate requests to your backend application with both valid and invalid requests.
