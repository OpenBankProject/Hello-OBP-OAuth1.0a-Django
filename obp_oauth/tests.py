from django.test import TestCase


class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        # for the test of Github Actions
        self.assertEqual(response.status_code, 200)
