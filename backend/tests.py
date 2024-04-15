import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_ocr(self):
        with open('test_image.jpg', 'rb') as file:
            response = self.app.post('/ocr', data={'image': (file, 'test_image.jpg')}, content_type='multipart/form-data')

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', data)
        self.assertIsInstance(data['text'], str)
        self.assertNotEqual(data['text'], '')

    def test_summarize(self):
        text = "This is a test text for summarization. It has multiple sentences to test the summarization function."
        response = self.app.post('/summarize', json={'text': text})

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('summary', data)
        self.assertIsInstance(data['summary'], str)
        self.assertNotEqual(data['summary'], '')

    def test_exportpdf(self):
        text = "This is a test text for PDF export. It should be included in the PDF document."
        summary = "This is a test summary for PDF export. It should also be included in the PDF document."
        data = {'text': text, 'summary': summary}

        response = self.app.post('/exportpdf', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_signup_new_user(self):
        credentials = {'username': 'new_unique_user', 'password': 'password'}
        response = self.app.post('/signup', json=credentials)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('isSuccessful', data)

        print(f"Signup Response Data: {data}")

        if 'isSuccessful' in data:
            self.assertTrue(data['isSuccessful'], f"Signup failed: {data.get('message', 'Unknown error')}")

    def test_login_non_existing_user(self):
        credentials = {'username': 'nonexistent', 'password': 'password'}
        response = self.app.post('/login', json=credentials)

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['isSuccessful'])
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'user does not exist')

    def test_signup_new_user(self):
        credentials = {'username': 'newuser', 'password': 'password'}
        response = self.app.post('/signup', json=credentials)

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['isSuccessful'])
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'signed up')

    def test_signup_existing_user(self):
        credentials = {'username': 'testuser', 'password': 'password'}
        response = self.app.post('/signup', json=credentials)

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['isSuccessful'])
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'username already taken')

if __name__ == '__main__':
    unittest.main()
