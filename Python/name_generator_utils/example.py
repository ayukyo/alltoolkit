#!/usr/bin/env python3
"""
Name Generator Utils - Usage Examples

This example demonstrates all the features of the name_generator_utils module.
Run with: python example.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from local module
from generator import (
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


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def main():
    """Demonstrate all name generator features."""
    
    # Create a generator with a seed for reproducible results
    gen = NameGenerator(seed=2026)
    
    print_section("First Names")
    print("Male first names:")
    for _ in range(5):
        print(f"  • {gen.first_name('male')}")
    
    print("\nFemale first names:")
    for _ in range(5):
        print(f"  • {gen.first_name('female')}")
    
    print("\nUnisex first names:")
    for _ in range(5):
        print(f"  • {gen.first_name('unisex')}")
    
    print("\nRandom first names (any gender):")
    for _ in range(5):
        print(f"  • {gen.first_name()}")
    
    print_section("Last Names")
    for _ in range(10):
        print(f"  • {gen.last_name()}")
    
    print_section("Full Names")
    print("Standard full names:")
    for _ in range(5):
        print(f"  • {gen.full_name()}")
    
    print("\nFull names with middle initial:")
    for _ in range(5):
        print(f"  • {gen.full_name(middle_initial=True)}")
    
    print("\nMale full names:")
    for _ in range(5):
        print(f"  • {gen.full_name(gender='male')}")
    
    print("\nFemale full names:")
    for _ in range(5):
        print(f"  • {gen.full_name(gender='female')}")
    
    print_section("Usernames")
    
    print("Simple style (firstname_lastname):")
    for _ in range(5):
        print(f"  • {gen.username('simple')}")
    
    print("\nProfessional style (firstname.lastname):")
    for _ in range(5):
        print(f"  • {gen.username('professional')}")
    
    print("\nGaming style:")
    for _ in range(5):
        print(f"  • {gen.username('gaming')}")
    
    print("\nSocial style (firstname + digits):")
    for _ in range(5):
        print(f"  • {gen.username('social')}")
    
    print_section("Codenames")
    
    print("Military style (Phonetic + Number):")
    for _ in range(5):
        print(f"  • {gen.codename('military')}")
    
    print("\nProject style (Adjective + Noun):")
    for _ in range(5):
        print(f"  • {gen.codename('project')}")
    
    print("\nAgent style:")
    for _ in range(5):
        print(f"  • {gen.codename('agent')}")
    
    print_section("Fantasy Names")
    
    print("Elf names (elegant, flowing):")
    for _ in range(5):
        print(f"  • {gen.fantasy_name('elf')}")
    
    print("\nDwarf names (strong, consonant-heavy):")
    for _ in range(5):
        print(f"  • {gen.fantasy_name('dwarf')}")
    
    print("\nHuman fantasy names:")
    for _ in range(5):
        print(f"  • {gen.fantasy_name('human')}")
    
    print("\nMystical names (ethereal):")
    for _ in range(5):
        print(f"  • {gen.fantasy_name('mystical')}")
    
    print_section("Company Names")
    for _ in range(10):
        print(f"  • {gen.company_name()}")
    
    print_section("Pet Names")
    
    print("Cute pet names:")
    for _ in range(5):
        print(f"  • {gen.pet_name('cute')}")
    
    print("\nFierce pet names:")
    for _ in range(5):
        print(f"  • {gen.pet_name('fierce')}")
    
    print("\nRandom pet names:")
    for _ in range(5):
        print(f"  • {gen.pet_name('random')}")
    
    print_section("Batch Generation")
    
    print("Generate 10 full names at once:")
    names = gen.batch(10, "full_name")
    for i, name in enumerate(names, 1):
        print(f"  {i:2d}. {name}")
    
    print("\nGenerate 5 project codenames:")
    codenames = gen.batch(5, "codename", style="project")
    for i, name in enumerate(codenames, 1):
        print(f"  {i}. {name}")
    
    print_section("Convenience Functions")
    
    print("Using module-level convenience functions:")
    print(f"  First name:      {generate_first_name()}")
    print(f"  Last name:       {generate_last_name()}")
    print(f"  Full name:       {generate_full_name()}")
    print(f"  Username:        {generate_username()}")
    print(f"  Codename:        {generate_codename()}")
    print(f"  Fantasy name:    {generate_fantasy_name()}")
    print(f"  Company name:    {generate_company_name()}")
    print(f"  Pet name:        {generate_pet_name()}")
    
    print_section("Practical Use Cases")
    
    print("\n📝 Generate a team of characters for a story:")
    print("  Protagonist:", gen.full_name("male"))
    print("  Love interest:", gen.full_name("female"))
    print("  Mentor:", gen.full_name(middle_initial=True))
    print("  Villain codename:", gen.codename("agent"))
    print("  Secret project:", gen.codename("project"))
    
    print("\n🎮 Generate gaming profiles:")
    for i in range(1, 4):
        print(f"  Player {i}: {gen.username('gaming')}")
    
    print("\n🏢 Generate company names for a fictional universe:")
    companies = gen.batch(5, "company_name")
    for name in companies:
        print(f"  • {name}")
    
    print("\n🐉 Generate fantasy RPG party:")
    print("  Elf Mage:", gen.fantasy_name("elf"))
    print("  Dwarf Warrior:", gen.fantasy_name("dwarf"))
    print("  Human Rogue:", gen.fantasy_name("human"))
    print("  Mysterious Being:", gen.fantasy_name("mystical"))
    
    print("\n🐕 Pet adoption scenario:")
    print("  Cute option:", gen.pet_name("cute"))
    print("  Fierce option:", gen.pet_name("fierce"))
    print("  Owner's name:", gen.full_name())
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()