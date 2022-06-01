import unittest
from unittest import TestCase
from app import app as tested_app
from app import views
import json

class TestNewsAdm(TestCase):
    def setUp(self):
        tested_app.config['TESTING'] = True
        self.app = tested_app.test_client()

    def test_index(self):
        r = self.app.get('/')
        return self.assertEqual(r.status_code, 200)

    def test_data(self):
        r = self.app.get('/api/data')
        self.assertGreater(len(r.json['data']), 10)

if __name__ == '__main__':
    unittest.main()