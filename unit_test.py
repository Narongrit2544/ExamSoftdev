import unittest
from app.app import app  # นำเข้า app จาก app.py

class PrimeTestCase(unittest.TestCase):

    def setUp(self):
        # สร้าง test client
        self.app = app.test_client()
        self.app.testing = True

    def true_when_x_is_17(self):
        # เรียกใช้ endpoint โดยใช้ test client
        response = self.app.get('/is_prime/17')
        self.assertEqual(response.json, {'is_prime': True})

    def false_when_x_is_36(self):
        # เรียกใช้ endpoint โดยใช้ test client
        response = self.app.get('/is_prime/36')
        self.assertEqual(response.json, {'is_prime': False})
    def true_when_x_is_13219(self):
        response = self.app.get('/is_prime/13219')
        self.assertEqual(response.json, {'is_prime': True})


if __name__ == '__main__':
    unittest.main()
