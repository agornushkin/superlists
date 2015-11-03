from django.test import TestCase

# Create your tests here.

class SmokeTest(TestCase):

    def test_failing(self):
        dz = 1/0