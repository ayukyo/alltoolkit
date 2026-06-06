"""
Tests for Name Generator Utils.

Run with: python -m pytest test_generator.py -v
Or simply: python test_generator.py

Compatible with Python 3.6+.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from name_generator_utils import (
    NameGenerator,
    generate_first_name,
    generate_last_name,
    generate_full_name,
    generate_username,
    generate_codename,
    generate_fantasy_name,
    generate_company_name,
    generate_pet_name,
)


class TestNameGenerator(unittest.TestCase):
    """Test cases for NameGenerator class."""
    
    def test_first_name_male(self):
        """Test generating male first names."""
        gen = NameGenerator(seed=42)
        name = gen.first_name("male")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        self.assertIn(name, NameGenerator.MALE_FIRST_NAMES)
    
    def test_first_name_female(self):
        """Test generating female first names."""
        gen = NameGenerator(seed=42)
        name = gen.first_name("female")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        self.assertIn(name, NameGenerator.FEMALE_FIRST_NAMES)
    
    def test_first_name_unisex(self):
        """Test generating unisex first names."""
        gen = NameGenerator(seed=42)
        name = gen.first_name("unisex")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        self.assertIn(name, NameGenerator.UNISEX_FIRST_NAMES)
    
    def test_first_name_any(self):
        """Test generating any first name."""
        gen = NameGenerator(seed=42)
        name = gen.first_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_last_name(self):
        """Test generating last names."""
        gen = NameGenerator(seed=42)
        name = gen.last_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        self.assertIn(name, NameGenerator.LAST_NAMES)
    
    def test_full_name(self):
        """Test generating full names."""
        gen = NameGenerator(seed=42)
        name = gen.full_name()
        self.assertIsInstance(name, str)
        parts = name.split()
        self.assertEqual(len(parts), 2)
        self.assertTrue(len(parts[0]) > 0)
        self.assertTrue(len(parts[1]) > 0)
    
    def test_full_name_with_middle_initial(self):
        """Test generating full names with middle initial."""
        gen = NameGenerator(seed=42)
        name = gen.full_name(middle_initial=True)
        self.assertIsInstance(name, str)
        parts = name.split()
        self.assertEqual(len(parts), 3)
        self.assertTrue(len(parts[0]) > 0)  # First name
        self.assertEqual(len(parts[1]), 2)   # Middle initial with dot
        self.assertTrue(parts[1].endswith('.'))
        self.assertTrue(len(parts[2]) > 0)  # Last name
    
    def test_full_name_gender(self):
        """Test generating full names with gender filter."""
        gen = NameGenerator(seed=42)
        for _ in range(10):
            name = gen.full_name(gender="male")
            first_name = name.split()[0]
            self.assertIn(first_name, NameGenerator.MALE_FIRST_NAMES + NameGenerator.UNISEX_FIRST_NAMES)
    
    def test_username_simple(self):
        """Test generating simple usernames."""
        gen = NameGenerator(seed=42)
        username = gen.username("simple")
        self.assertIsInstance(username, str)
        self.assertIn("_", username)
        self.assertTrue(username.islower() or username.replace("_", "").isalpha())
    
    def test_username_professional(self):
        """Test generating professional usernames."""
        gen = NameGenerator(seed=42)
        username = gen.username("professional")
        self.assertIsInstance(username, str)
        self.assertIn(".", username)
    
    def test_username_gaming(self):
        """Test generating gaming usernames."""
        gen = NameGenerator(seed=42)
        username = gen.username("gaming")
        self.assertIsInstance(username, str)
        self.assertTrue(len(username) > 0)
    
    def test_username_social(self):
        """Test generating social usernames."""
        gen = NameGenerator(seed=42)
        username = gen.username("social")
        self.assertIsInstance(username, str)
        self.assertTrue(any(c.isdigit() for c in username))
    
    def test_codename_military(self):
        """Test generating military codenames."""
        gen = NameGenerator(seed=42)
        codename = gen.codename("military")
        self.assertIsInstance(codename, str)
        parts = codename.split()
        self.assertEqual(len(parts), 2)
    
    def test_codename_project(self):
        """Test generating project codenames."""
        gen = NameGenerator(seed=42)
        codename = gen.codename("project")
        self.assertIsInstance(codename, str)
        parts = codename.split()
        self.assertGreaterEqual(len(parts), 2)
    
    def test_codename_agent(self):
        """Test generating agent codenames."""
        gen = NameGenerator(seed=42)
        codename = gen.codename("agent")
        self.assertIsInstance(codename, str)
        self.assertIn("Agent", codename)
    
    def test_fantasy_name_elf(self):
        """Test generating elf fantasy names."""
        gen = NameGenerator(seed=42)
        name = gen.fantasy_name("elf")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_fantasy_name_dwarf(self):
        """Test generating dwarf fantasy names."""
        gen = NameGenerator(seed=42)
        name = gen.fantasy_name("dwarf")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_fantasy_name_human(self):
        """Test generating human fantasy names."""
        gen = NameGenerator(seed=42)
        name = gen.fantasy_name("human")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_fantasy_name_mystical(self):
        """Test generating mystical fantasy names."""
        gen = NameGenerator(seed=42)
        name = gen.fantasy_name("mystical")
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_company_name(self):
        """Test generating company names."""
        gen = NameGenerator(seed=42)
        name = gen.company_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        # Should have at least two parts (prefix + suffix)
        parts = name.split()
        self.assertGreaterEqual(len(parts), 2)
    
    def test_pet_name_cute(self):
        """Test generating cute pet names."""
        gen = NameGenerator(seed=42)
        name = gen.pet_name("cute")
        self.assertIsInstance(name, str)
        self.assertIn(name, NameGenerator.PET_NAMES_CUTE)
    
    def test_pet_name_fierce(self):
        """Test generating fierce pet names."""
        gen = NameGenerator(seed=42)
        name = gen.pet_name("fierce")
        self.assertIsInstance(name, str)
        self.assertIn(name, NameGenerator.PET_NAMES_FIERCE)
    
    def test_pet_name_random(self):
        """Test generating random pet names."""
        gen = NameGenerator(seed=42)
        name = gen.pet_name("random")
        self.assertIsInstance(name, str)
        self.assertIn(
            name, 
            NameGenerator.PET_NAMES_CUTE + NameGenerator.PET_NAMES_FIERCE
        )
    
    def test_batch_full_names(self):
        """Test generating batch of full names."""
        gen = NameGenerator(seed=42)
        names = gen.batch(5, "full_name")
        self.assertEqual(len(names), 5)
        for name in names:
            self.assertIsInstance(name, str)
            self.assertEqual(len(name.split()), 2)
    
    def test_batch_usernames(self):
        """Test generating batch of usernames."""
        gen = NameGenerator(seed=42)
        names = gen.batch(3, "username", style="simple")
        self.assertEqual(len(names), 3)
        for name in names:
            self.assertIn("_", name)
    
    def test_batch_invalid_method(self):
        """Test batch with invalid method."""
        gen = NameGenerator(seed=42)
        with self.assertRaises(ValueError):
            gen.batch(3, "invalid_method")
    
    def test_reproducible_with_seed(self):
        """Test that same seed produces same results."""
        gen1 = NameGenerator(seed=12345)
        gen2 = NameGenerator(seed=12345)
        
        for _ in range(10):
            self.assertEqual(gen1.first_name(), gen2.first_name())
            self.assertEqual(gen1.last_name(), gen2.last_name())
    
    def test_different_seeds_produce_different_results(self):
        """Test that different seeds produce different results."""
        gen1 = NameGenerator(seed=111)
        gen2 = NameGenerator(seed=222)
        
        names1 = [gen1.full_name() for _ in range(10)]
        names2 = [gen2.full_name() for _ in range(10)]
        
        self.assertNotEqual(names1, names2)
    
    def test_no_external_dependencies(self):
        """Test that the module uses only standard library."""
        # This test verifies the implementation uses only stdlib
        import name_generator_utils.generator as gen_module
        
        source = gen_module.__file__
        with open(source, 'r') as f:
            content = f.read()
        
        # Check for common external dependency imports
        forbidden = ['import numpy', 'import pandas', 'import requests',
                     'from numpy', 'from pandas', 'from requests']
        
        for dep in forbidden:
            self.assertNotIn(dep, content, 
                           f"External dependency found: {dep}")


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_generate_first_name(self):
        """Test generate_first_name convenience function."""
        name = generate_first_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_generate_last_name(self):
        """Test generate_last_name convenience function."""
        name = generate_last_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_generate_full_name(self):
        """Test generate_full_name convenience function."""
        name = generate_full_name()
        self.assertIsInstance(name, str)
        self.assertEqual(len(name.split()), 2)
    
    def test_generate_username(self):
        """Test generate_username convenience function."""
        username = generate_username()
        self.assertIsInstance(username, str)
        self.assertTrue(len(username) > 0)
    
    def test_generate_codename(self):
        """Test generate_codename convenience function."""
        codename = generate_codename()
        self.assertIsInstance(codename, str)
        self.assertTrue(len(codename) > 0)
    
    def test_generate_fantasy_name(self):
        """Test generate_fantasy_name convenience function."""
        name = generate_fantasy_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_generate_company_name(self):
        """Test generate_company_name convenience function."""
        name = generate_company_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
    
    def test_generate_pet_name(self):
        """Test generate_pet_name convenience function."""
        name = generate_pet_name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)