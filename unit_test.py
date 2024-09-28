import unittest
from app.app import app  # นำเข้า app จาก app.py

class PrimeTestCase(unittest.TestCase):

    def setUp(self):
        # สร้าง test client
        self.app = app.test_client()
        self.app.testing = True

    def test_is_prime_true(self):
        # เรียกใช้ endpoint โดยใช้ test client
        response = self.app.get('/is_prime/29')
        self.assertEqual(response.json, {'is_prime': True})

    def test_is_prime_false(self):
        # เรียกใช้ endpoint โดยใช้ test client
        response = self.app.get('/is_prime/1')
        self.assertEqual(response.json, {'is_prime': False})

if __name__ == '__main__':
    unittest.main()
