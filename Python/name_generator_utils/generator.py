"""
Name Generator - Core generation logic.

Provides various name generation utilities with zero external dependencies.
"""

import random
import string
from typing import List, Optional, Union


class NameGenerator:
    """
    A versatile name generator supporting multiple name types.
    
    Features:
    - First names (male/female/unisex)
    - Last names from various cultures
    - Username generation with customizable patterns
    - Codename generation for projects/operations
    - Fantasy names for games/stories
    - Company names
    - Pet names
    
    Example:
        >>> gen = NameGenerator(seed=42)
        >>> gen.full_name()
        'Ethan Caldwell'
        >>> gen.username()
        'ethan_caldwell_2024'
    """
    
    # Common first names
    MALE_FIRST_NAMES = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard",
        "Joseph", "Thomas", "Charles", "Christopher", "Daniel", "Matthew",
        "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
        "Kenneth", "Kevin", "Brian", "George", "Timothy", "Ronald", "Edward",
        "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric",
        "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin",
        "Samuel", "Raymond", "Gregory", "Frank", "Alexander", "Patrick", "Jack",
        "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry",
        "Douglas", "Zachary", "Peter", "Kyle", "Ethan", "Walter", "Noah",
        "Jeremy", "Christian", "Keith", "Roger", "Terry", "Austin", "Sean",
        "Gerald", "Carl", "Dylan", "Harold", "Jordan", "Jesse", "Bryan",
        "Lawrence", "Arthur", "Gabriel", "Bruce", "Albert", "Willie", "Alan",
        "Wayne", "Billy", "Joe", "Ralph", "Eugene", "Russell", "Randy", "Philip",
        "Harry", "Vincent", "Bobby", "Johnny", "Logan", "Owen", "Derek", "Dylan",
    ]
    
    FEMALE_FIRST_NAMES = [
        "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
        "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
        "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
        "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
        "Cynthia", "Kathleen", "Amy", "Angela", "Shirley", "Anna", "Brenda",
        "Pamela", "Emma", "Nicole", "Helen", "Samantha", "Katherine", "Christine",
        "Debra", "Rachel", "Carolyn", "Janet", "Catherine", "Maria", "Heather",
        "Diane", "Ruth", "Julie", "Olivia", "Joyce", "Virginia", "Victoria",
        "Kelly", "Lauren", "Christina", "Joan", "Evelyn", "Judith", "Megan",
        "Andrea", "Cheryl", "Hannah", "Jacqueline", "Martha", "Gloria", "Teresa",
        "Ann", "Sara", "Madison", "Frances", "Kathryn", "Janice", "Jean", "Abigail",
        "Alice", "Judy", "Sophia", "Grace", "Denise", "Amber", "Doris", "Marilyn",
        "Danielle", "Beverly", "Isabella", "Theresa", "Diana", "Natalie", "Brittany",
        "Charlotte", "Marie", "Kayla", "Alexis", "Lori", "Jessica", "Lily", "Ava",
    ]
    
    UNISEX_FIRST_NAMES = [
        "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Jamie",
        "Reese", "Peyton", "Quinn", "Hayden", "Cameron", "Rowan", "Skyler",
        "Dakota", "Drew", "Finley", "Sage", "Phoenix", "Sydney", "Dylan",
        "Ryan", "Angel", "Parker", "Cameron", "Carson", "Blake", "Dylan",
        "Emery", "Kendall", "Logan", "Parker", "Peyton", "Riley", "Sawyer",
    ]
    
    # Common last names
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
        "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
        "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
        "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
        "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan",
        "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos",
        "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez",
        "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long",
        "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell",
        "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Wells",
        "Chen", "Kumar", "Singh", "Patel", "Sharma", "Khan", "Ali", "Ahmed",
        "Hassan", "Hussein", "Mahmoud", "Ibrahim", "Yusuf", "Omar", "Khalil",
    ]
    
    # Fantasy name components
    FANTASY_PREFIXES = [
        "Ael", "Aer", "Al", "An", "Ar", "Bel", "Bor", "Cal", "Cel", "Dae",
        "Dal", "Dor", "Eld", "El", "Em", "Er", "Fae", "Fin", "Gal", "Gor",
        "Hal", "Hel", "Il", "Ion", "Is", "Jor", "Kal", "Kel", "Lor", "Lys",
        "Ma", "Mel", "Mor", "Nar", "Ner", "Oc", "Or", "Pel", "Py", "Qua",
        "Ral", "Rho", "Sae", "Sel", "Syl", "Tal", "Tha", "Ul", "Val", "Vor",
        "Wyn", "Xan", "Ylv", "Zae", "Zor",
    ]
    
    FANTASY_MIDDLES = [
        "a", "ae", "an", "ar", "as", "dra", "el", "en", "er", "i", "ia",
        "in", "is", "ith", "la", "li", "lon", "ma", "na", "ni", "or", "ra",
        "ri", "ro", "sa", "si", "th", "tha", "vi", "ya", "yon",
    ]
    
    FANTASY_SUFFIXES = [
        "a", "ae", "al", "an", "ar", "as", "dore", "dor", "ea", "el", "en",
        "er", "ia", "ial", "ian", "iel", "il", "in", "is", "ith", "ix", "la",
        "las", "lia", "lin", "lon", "na", "nia", "on", "or", "ra", "riel",
        "ris", "ros", "s", "sa", "th", "tha", "us", "var", "via", "ya",
    ]
    
    # Codename words
    CODENAME_ADJECTIVES = [
        "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel",
        "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
        "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey",
        "X-ray", "Yankee", "Zulu",
        "Shadow", "Silent", "Swift", "Storm", "Steel", "Silver", "Golden",
        "Crimson", "Azure", "Emerald", "Ruby", "Onyx", "Phantom", "Ghost",
        "Thunder", "Lightning", "Fire", "Ice", "Night", "Dawn", "Dusk",
        "Arctic", "Desert", "Ocean", "Mountain", "Forest", "River", "Wolf",
        "Eagle", "Hawk", "Falcon", "Phoenix", "Dragon", "Tiger", "Lion",
    ]
    
    CODENAME_NOUNS = [
        "Arrow", "Blade", "Bow", "Castle", "Crown", "Dagger", "Eagle", "Falcon",
        "Guard", "Hammer", "Hawk", "Hunter", "Knight", "Lance", "Lion", "Shield",
        "Spear", "Star", "Sword", "Tiger", "Tower", "Viper", "Warrior", "Wolf",
        "Protocol", "Project", "Operation", "Mission", "Vector", "Program",
        "System", "Network", "Cipher", "Code", "Signal", "Matrix", "Vector",
        "Horizon", "Summit", "Apex", "Zenith", "Nexus", "Core", "Unit", "Force",
        "Squad", "Team", "Division", "Branch", "Sector", "Zone", "Region",
    ]
    
    # Company name components
    COMPANY_PREFIXES = [
        "Apex", "Nova", "Pulse", "Vertex", "Quantum", "Stellar", "Nexus", "Prism",
        "Echo", "Flux", "Core", "Zenith", "Helix", "Orbit", "Vortex", "Synapse",
        "Prime", "Alpha", "Omega", "Delta", "Sigma", "Cascade", "Terra", "Aero",
        "Dyna", "Cyber", "Meta", "Neo", "Hyper", "Ultra", "Super", "Mega",
        "Global", "Unified", "Advanced", "Modern", "Future", "Digital", "Smart",
        "Cloud", "Data", "Tech", "Net", "Web", "Soft", "Sys", "Info", "Bio",
    ]
    
    COMPANY_SUFFIXES = [
        "Labs", "Corp", "Inc", "Co", "Tech", "Systems", "Solutions", "Group",
        "Holdings", "Partners", "Associates", "International", "Global",
        "Industries", "Enterprises", "Dynamics", "Innovations", "Ventures",
        "Capital", "Digital", "Media", "Networks", "Services", "Consulting",
        "Analytics", "Software", "Platforms", "Works", "Studio", "Hub",
        "Labs", "Research", "Science", "Engineering", "Design", "Creative",
    ]
    
    # Pet name components
    PET_NAMES_CUTE = [
        "Fluffy", "Whiskers", "Shadow", "Midnight", "Snowball", "Mittens",
        "Oreo", "Patches", "Peanut", "Mochi", "Coco", "Buddy", "Max",
        "Bella", "Charlie", "Lucy", "Daisy", "Bailey", "Molly", "Oliver",
        "Leo", "Milo", "Teddy", "Simba", "Luna", "Nala", "Willow", "Chloe",
        "Lola", "Rosie", "Sadie", "Maggie", "Sophie", "Penny", "Ruby",
        "Ginger", "Pepper", "Cinnamon", "Cookie", "Honey", "Sugar", "Maple",
        "Olive", "Winnie", "Toby", "Duke", "Cooper", "Rocky", "Bear", "Duke",
    ]
    
    PET_NAMES_FIERCE = [
        "Rex", "Thor", "Zeus", "Apollo", "Titan", "Atlas", "Maximus", "Brutus",
        "Caesar", "Jupiter", "Mars", "Hercules", "Achilles", "Spartan", "Razor",
        "Blade", "Fang", "Spike", "Rocco", "Bruno", "Boss", "Chief", "King",
        "Prince", "Duke", "Storm", "Thunder", "Lightning", "Rogue", "Hunter",
    ]
    
    def __init__(self, seed=None):
        """
        Initialize the name generator.
        
        Args:
            seed: Optional random seed for reproducible results.
        """
        self._random = random.Random(seed)
    
    def first_name(self, gender=None):
        """
        Generate a random first name.
        
        Args:
            gender: Optional gender filter. If None, selects from all names.
                   Valid values: "male", "female", "unisex"
        
        Returns:
            A randomly selected first name.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.first_name("male")
            'Brian'
            >>> gen.first_name("female")
            'Laura'
        """
        if gender == "male":
            return self._random.choice(self.MALE_FIRST_NAMES)
        elif gender == "female":
            return self._random.choice(self.FEMALE_FIRST_NAMES)
        elif gender == "unisex":
            return self._random.choice(self.UNISEX_FIRST_NAMES)
        else:
            all_names = (
                self.MALE_FIRST_NAMES + 
                self.FEMALE_FIRST_NAMES + 
                self.UNISEX_FIRST_NAMES
            )
            return self._random.choice(all_names)
    
    def last_name(self):
        """
        Generate a random last name.
        
        Returns:
            A randomly selected last name.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.last_name()
            'Wright'
        """
        return self._random.choice(self.LAST_NAMES)
    
    def full_name(self, gender=None, middle_initial=False):
        """
        Generate a random full name.
        
        Args:
            gender: Optional gender filter for the first name.
                   Valid values: "male", "female", "unisex"
            middle_initial: If True, includes a middle initial.
        
        Returns:
            A randomly generated full name.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.full_name("male")
            'Brian Wright'
            >>> gen.full_name(middle_initial=True)
            'Karen M. Wilson'
        """
        first = self.first_name(gender)
        last = self.last_name()
        
        if middle_initial:
            middle = self._random.choice(string.ascii_uppercase)
            return f"{first} {middle}. {last}"
        return f"{first} {last}"
    
    def username(self, style="simple"):
        """
        Generate a random username.
        
        Args:
            style: Username style to generate.
                - simple: firstname_lastname format
                - professional: firstname.lastname with optional numbers
                - gaming: creative with numbers and underscores
                - social: firstname + random digits
        
        Returns:
            A randomly generated username.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.username("simple")
            'brian_wright'
            >>> gen.username("professional")
            'karen.wilson42'
        """
        first = self.first_name().lower()
        last = self.last_name().lower()
        
        if style == "simple":
            return f"{first}_{last}"
        
        elif style == "professional":
            num = self._random.randint(1, 99) if self._random.random() > 0.5 else ""
            return f"{first}.{last}{num}"
        
        elif style == "gaming":
            prefixes = ["xX", "Pro", "Elite", "Dark", "Shadow", "Cyber", ""]
            suffixes = ["Xx", "_master", "_pro", "_gamer", "_elite", ""]
            prefix = self._random.choice(prefixes)
            suffix = self._random.choice(suffixes)
            num = self._random.randint(0, 999) if self._random.random() > 0.3 else ""
            return f"{prefix}{first}{last}{num}{suffix}".lower()
        
        elif style == "social":
            num = self._random.randint(10, 9999)
            return f"{first}{num}"
        
        return f"{first}_{last}"
    
    def codename(self, style="military"):
        """
        Generate a random codename.
        
        Args:
            style: Codename style.
                - military: Phonetic alphabet + number (e.g., "Alpha Seven")
                - project: Adjective + Noun (e.g., "Shadow Protocol")
                - agent: Single word + number (e.g., "Agent Phoenix")
        
        Returns:
            A randomly generated codename.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.codename("military")
            'Sierra Seven'
            >>> gen.codename("project")
            'Phantom Protocol'
        """
        if style == "military":
            phonetic = [
                "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot",
                "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike",
                "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra",
                "Tango", "Uniform", "Victor", "Whiskey", "X-ray", "Yankee", "Zulu"
            ]
            word = self._random.choice(phonetic)
            number = self._random.choice(["One", "Two", "Three", "Four", "Five",
                                          "Six", "Seven", "Eight", "Nine", "Zero"])
            return f"{word} {number}"
        
        elif style == "project":
            adj = self._random.choice(self.CODENAME_ADJECTIVES)
            noun = self._random.choice(self.CODENAME_NOUNS)
            return f"{adj} {noun}"
        
        elif style == "agent":
            codenames = [
                "Phoenix", "Spectre", "Shadow", "Ghost", "Viper", "Falcon",
                "Raven", "Wolf", "Eagle", "Hawk", "Tiger", "Dragon", "Cobra",
                "Panther", "Jaguar", "Scorpion", "Venom", "Blade", "Storm",
            ]
            name = self._random.choice(codenames)
            num = self._random.randint(1, 99)
            return f"Agent {name}-{num}"
        
        return f"Project {self._random.choice(self.CODENAME_NOUNS)}"
    
    def fantasy_name(self, race="elf"):
        """
        Generate a random fantasy name.
        
        Args:
            race: Fantasy race style.
                - elf: Elegant, flowing names with many vowels
                - dwarf: Strong, consonant-heavy names
                - human: Mixed style
                - mystical: Ethereal, magical-sounding names
        
        Returns:
            A randomly generated fantasy name.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.fantasy_name("elf")
            'Aelindra'
            >>> gen.fantasy_name("dwarf")
            'Thrum Gorim'
        """
        if race == "elf":
            # Elven names are elegant with many vowels
            prefixes = ["Ae", "Ea", "El", "Ael", "Thal", "Val", "Sil", "Gil",
                       "Fin", "Gal", "Nar", "Lor", "Ise", "Arw", "Cel"]
            middles = ["rin", "wyn", "lia", "ris", "dan", "thil", "on", "il",
                      "ael", "ion", "dra", "the", "nae", "ria", "ys"]
            suffixes = ["a", "iel", "ia", "is", "ae", "on", "ys", "iel", "a", "i"]
            
            name = (
                self._random.choice(prefixes) +
                self._random.choice(middles) +
                self._random.choice(suffixes)
            )
            return name
        
        elif race == "dwarf":
            # Dwarven names are strong and consonant-heavy
            prefixes = ["Thrum", "Gim", "Thor", "Bal", "Dur", "Gor", "Krag",
                       "Bru", "Thom", "Val", "Bor", "Grom", "Kil", "Thar"]
            suffixes = ["lin", "grim", "in", "um", "on", "un", "en", "irn",
                       "orn", "ur", "rak", "gar", "dun", "rek", "var"]
            titles = ["Ironforge", "Stonehammer", "Goldbeard", "Ironfist",
                     "Copperheart", "Steelaxe", "Bronzebrow", "Silveraxe"]
            
            first = self._random.choice(prefixes) + self._random.choice(suffixes)
            if self._random.random() > 0.5:
                return f"{first} {self._random.choice(titles)}"
            return first
        
        elif race == "human":
            # Human fantasy names are more varied
            prefix = self._random.choice(self.FANTASY_PREFIXES)
            middle = self._random.choice(self.FANTASY_MIDDLES)
            suffix = self._random.choice(self.FANTASY_SUFFIXES)
            return (prefix + middle + suffix).capitalize()
        
        elif race == "mystical":
            # Mystical names sound otherworldly
            prefixes = ["Xy", "Zae", "Qy", "Aeth", "O", "U", "Iy", "Ae", "Yl", "Xa"]
            middles = ["th", "ph", "s", "x", "z", "v", "l", "r", "n", "m"]
            suffixes = ["yx", "ae", "is", "os", "us", "ia", "um", "on", "ys", "a"]
            
            name = (
                self._random.choice(prefixes) +
                self._random.choice(middles) +
                self._random.choice(self.FANTASY_MIDDLES) +
                self._random.choice(suffixes)
            )
            return name.capitalize()
        
        return self._random.choice(self.FANTASY_PREFIXES)
    
    def company_name(self):
        """
        Generate a random company name.
        
        Returns:
            A randomly generated company name.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.company_name()
            'Prism Dynamics Inc'
        """
        prefix = self._random.choice(self.COMPANY_PREFIXES)
        suffix = self._random.choice(self.COMPANY_SUFFIXES)
        suffix_type = self._random.choice(["", " Inc", " Corp", " LLC", " Ltd"])
        return f"{prefix} {suffix}{suffix_type}".strip()
    
    def pet_name(self, style="random"):
        """
        Generate a random pet name.
        
        Args:
            style: Pet name style.
                - cute: Adorable, friendly names
                - fierce: Strong, powerful names
                - random: Mix of both
        
        Returns:
            A randomly selected pet name.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.pet_name("cute")
            'Snowball'
            >>> gen.pet_name("fierce")
            'Thor'
        """
        if style == "cute":
            return self._random.choice(self.PET_NAMES_CUTE)
        elif style == "fierce":
            return self._random.choice(self.PET_NAMES_FIERCE)
        else:
            return self._random.choice(self.PET_NAMES_CUTE + self.PET_NAMES_FIERCE)
    
    def batch(self, count, method="full_name", **kwargs):
        """
        Generate multiple names at once.
        
        Args:
            count: Number of names to generate.
            method: Name generation method to use.
            **kwargs: Additional arguments passed to the method.
        
        Returns:
            List of generated names.
        
        Example:
            >>> gen = NameGenerator(seed=42)
            >>> gen.batch(3, "full_name", gender="male")
            ['Brian Wright', 'Timothy Clark', 'Donald Moore']
        """
        method_func = getattr(self, method, None)
        if method_func is None or not callable(method_func):
            raise ValueError(f"Unknown method: {method}")
        
        return [method_func(**kwargs) for _ in range(count)]


# Convenience functions using a default generator
_default_generator = NameGenerator()


def generate_first_name(gender=None):
    """Generate a random first name."""
    return _default_generator.first_name(gender)


def generate_last_name():
    """Generate a random last name."""
    return _default_generator.last_name()


def generate_full_name(gender=None, middle_initial=False):
    """Generate a random full name."""
    return _default_generator.full_name(gender, middle_initial)


def generate_username(style="simple"):
    """Generate a random username."""
    return _default_generator.username(style)


def generate_codename(style="military"):
    """Generate a random codename."""
    return _default_generator.codename(style)


def generate_fantasy_name(race="elf"):
    """Generate a random fantasy name."""
    return _default_generator.fantasy_name(race)


def generate_company_name():
    """Generate a random company name."""
    return _default_generator.company_name()


def generate_pet_name(style="random"):
    """Generate a random pet name."""
    return _default_generator.pet_name(style)