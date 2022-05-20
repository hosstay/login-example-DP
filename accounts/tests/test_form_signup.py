from django.test import TestCase

from ..forms import RegisterForm

class RegisterFormTest(TestCase):
    def test_form_has_fields(self):
        form = RegisterForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)