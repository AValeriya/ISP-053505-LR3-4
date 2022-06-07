from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.db import models
from django.test import TestCase

# Create your tests here.

class TestAuthentification(TestCase):

    def test_registration(self):
        form_data = {'username': "Nina", 'password1': "qwer05350113", 'password2': "qwer05350113"}
        response = self.client.post("/Register", data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        form_data = {'username': "Ngd", 'password': "qwer"}
        response = self.client.post("/login", data=form_data)
        self.assertEqual(response.status_code, 200)
