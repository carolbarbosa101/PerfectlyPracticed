from django.test import TestCase

class DashboardTest(TestCase):

    def test_uses_dashboard_template(self):
        response = self.client.get('/dashboard')
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
