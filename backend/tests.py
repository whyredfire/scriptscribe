import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_ocr(self):
        with open('test_image.jpg', 'rb') as file:
            response = self.app.post('/ocr', data={'image': file}, content_type='multipart/form-data')

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', data)

    def test_summarize(self):
        text = "This is a test text for summarization. It has multiple sentences to test the summarization function."
        response = self.app.post('/summarize', json={'text': text})

        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('summary', data)

    def test_exportpdf(self):
        text = "This is a test text for PDF export. It should be included in the PDF document."
        summary = "This is a test summary for PDF export. It should also be included in the PDF document."
        data = {'text': text, 'summary': summary}

        response = self.app.post('/exportpdf', json=data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
