from django.test import TestCase
from .utils import generate_password

class PasswordGeneratorTests(TestCase):
    
    def test_default_generation(self):
        password = generate_password()
        self.assertEqual(len(password), 16)
        
    def test_length_customisation(self):
        password = generate_password(length=24)
        self.assertEqual(len(password), 24)
        
    def test_exclude_ambiguous(self):
        # Generate multiple times to ensure probability catches any errors
        for _ in range(100):
            password = generate_password(exclude_ambiguous=True)
            for char in "il1Lo0O":
                self.assertNotIn(char, password)
                
    def test_no_character_types_selected(self):
        with self.assertRaises(ValueError):
            generate_password(
                include_upper=False, 
                include_lower=False, 
                include_numbers=False, 
                include_symbols=False
            )
            
    def test_guaranteed_characters(self):
        password = generate_password(
            length=4,
            include_upper=True,
            include_lower=True,
            include_numbers=True,
            include_symbols=True
        )
        # Check that at least one of each required character type exists
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))