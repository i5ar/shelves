from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

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

    @classmethod
    def setUpClass(cls):
        """Create users."""
        usernames = ['Gumbys', 'Rabbit of Caerbannog', 'Black Knight']
        cls.users = [User.objects.create(username=i) for i in usernames]

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_string_representation(self):
        """
        The string representation of the model must be the ``code`` field
        to match the API endpoint.

        """
        authors = self.users
        codes = [0, 'patsy']
        for code in codes:
            customer = Customer.objects.create(code=code, author=authors[0])
            self.assertEqual(str(customer), str(customer.code))

    def test_pk_field(self):
        self.assertTrue(
            Customer._meta.get_field('uuid').primary_key,
            msg='Good job... Breaking the front-end!'
        )

    def test_blank_fields(self):
        self.assertFalse(Customer._meta.get_field('author').blank)
        self.assertFalse(Customer._meta.get_field('code').blank)

    def test_unique_fields(self):
        customer = {'author': self.users[0], 'code': 'patsy'}
        Customer.objects.create(**customer)
        with self.assertRaises(IntegrityError):
            Customer.objects.create(**customer)
