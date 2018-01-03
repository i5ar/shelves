from django.test import TestCase
from django.contrib.auth.models import User
# from django.urls import reverse, resolve

# from requests.auth import HTTPBasicAuth

# from rest_framework import status
# from rest_framework.test import (
#     force_authenticate,
#     RequestsClient,
#     APITestCase,
#     APIRequestFactory,
#     APIClient
# )

from .models import Customer
# from .api.serializers import CustomerBinderSerializer, BinderSerializer


class CustomerTestCase(TestCase):

    def _create_users(self, *usernames):
        users = [User.objects.create(username=i) for i in usernames]
        return users

    def test_string_representation(self):
        """The string representation must always be the ``id``.

        Follow the KISS principle since working with API endpoints.

        """
        authors = self._create_users('monthy')
        codes = [0, 'egg and spam']
        for code in codes:
            customer = Customer.objects.create(code=code, author=authors[0])
            self.assertEqual(str(customer), str(customer.id))

    def test_unique_field(self):
        """
        Required fields:

        - ``author``;
        - ``code``.

        Optional fields:

        - ``name``.

        """
        self.assertTrue(Customer._meta.get_field('code').unique)
        self.assertFalse(
            Customer._meta.get_field('code').null,
            msg="The code field cannot be null, "
                "the binder serializer breaks otherwise."
        )
