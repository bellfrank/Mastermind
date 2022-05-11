from django.test import TestCase, Client

# Create your tests here.
class PageTestCase(TestCase):
    
    def test_index(self):
        c = Client()
        response = c.get("/mastergame/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["score"], 0)
        self.assertEqual(response.context["attempts"], 10)
        self.assertEqual(response.context["tasks"], [])

    def test_register(self):
        c = Client()
        response = c.get("/mastergame/register")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        c = Client()
        response = c.get("/mastergame/login")
        self.assertEqual(response.status_code, 200)

    def test_invalid(self):
        c = Client()
        response = c.get("/mastergame/hacking")
        self.assertEqual(response.status_code, 404)