import unittest
from app import app  

class PrimeTestCase(unittest.TestCase):

    def true_when_x_is_17(self):

        response = app.show_number('/is_prime/17')
        self.assertEqual(response, {'is_prime': True})

    def false_when_x_is_36(self):
        
        response = app.show_number('/is_prime/36')
        self.assertEqual(response, {'is_prime': False})
    def true_when_x_is_13219(self):
        
        response = app.show_number('/is_prime/13219')
        self.assertEqual(response, {'is_prime': True})


if __name__ == '__main__':
    unittest.main()
