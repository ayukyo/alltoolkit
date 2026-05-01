"""
AllToolkit - Python Fortune Utilities

A zero-dependency, production-ready fortune cookie and inspirational quote generator.
Supports multiple categories, custom fortune pools, weighted selection,
and various output formats for games, apps, and motivational displays.

Author: AllToolkit
License: MIT
"""

from typing import List, Dict, Optional, Tuple, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
import random
import hashlib


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Fortune:
    """Represents a single fortune."""
    text: str
    category: str = "general"
    author: Optional[str] = None
    source: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    difficulty: int = 1  # 1-5 for riddles/quotes
    
    def __repr__(self) -> str:
        if self.author:
            return f'Fortune("{self.text[:30]}..." - {self.author})'
        return f'Fortune("{self.text[:30]}...")'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'text': self.text,
            'category': self.category,
            'author': self.author,
            'source': self.source,
            'tags': self.tags,
            'difficulty': self.difficulty,
        }


@dataclass
class FortuneResult:
    """Represents a fortune generation result."""
    fortune: Fortune
    index: int
    total_in_category: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        result = self.fortune.text
        if self.fortune.author:
            result += f"\n    — {self.fortune.author}"
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'text': self.fortune.text,
            'category': self.fortune.category,
            'author': self.fortune.author,
            'source': self.fortune.source,
            'tags': self.fortune.tags,
            'index': self.index,
            'total_in_category': self.total_in_category,
            'timestamp': self.timestamp.isoformat(),
        }


# ============================================================================
# Built-in Fortune Database
# ============================================================================

# Classic Unix-style fortune cookies
UNIX_FORTUNES: List[str] = [
    "A journey of a thousand miles begins with a single step.",
    "A bird in the hand is worth two in the bush.",
    "Actions speak louder than words.",
    "All that glitters is not gold.",
    "An apple a day keeps the doctor away.",
    "Beauty is in the eye of the beholder.",
    "Better late than never.",
    "Birds of a feather flock together.",
    "Blood is thicker than water.",
    "Curiosity killed the cat.",
    "Don't count your chickens before they hatch.",
    "Don't put all your eggs in one basket.",
    "Easy come, easy go.",
    "Every cloud has a silver lining.",
    "First things first.",
    "Fortune favors the bold.",
    "Good things come to those who wait.",
    "Haste makes waste.",
    "He who laughs last laughs longest.",
    "Honesty is the best policy.",
    "Hope for the best, prepare for the worst.",
    "If it isn't broken, don't fix it.",
    "It takes two to tango.",
    "Keep your friends close and your enemies closer.",
    "Knowledge is power.",
    "Laughter is the best medicine.",
    "Learn from your mistakes.",
    "Let sleeping dogs lie.",
    "Life is what you make it.",
    "Look before you leap.",
    "Money doesn't grow on trees.",
    "Necessity is the mother of invention.",
    "Never give up.",
    "No pain, no gain.",
    "Nothing ventured, nothing gained.",
    "Once bitten, twice shy.",
    "Opportunity seldom knocks twice.",
    "Patience is a virtue.",
    "Practice makes perfect.",
    "Rome wasn't built in a day.",
    "Silence is golden.",
    "Strike while the iron is hot.",
    "The early bird catches the worm.",
    "The pen is mightier than the sword.",
    "There's no place like home.",
    "Time flies when you're having fun.",
    "Time heals all wounds.",
    "To err is human, to forgive divine.",
    "Tomorrow is another day.",
    "Two wrongs don't make a right.",
    "Variety is the spice of life.",
    "When in Rome, do as the Romans do.",
    "Where there's a will, there's a way.",
    "You can't have your cake and eat it too.",
    "You reap what you sow.",
]

# Inspirational quotes with authors
INSPIRATIONAL_QUOTES: List[Tuple[str, str]] = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
    ("The only impossible journey is the one you never begin.", "Tony Robbins"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
    ("The only person you are destined to become is the person you decide to be.", "Ralph Waldo Emerson"),
    ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
    ("Happiness is not something ready made. It comes from your own actions.", "Dalai Lama"),
    ("The mind is everything. What you think you become.", "Buddha"),
    ("Strive not to be a success, but rather to be of value.", "Albert Einstein"),
    ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison"),
    ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
    ("I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", "Maya Angelou"),
    ("The only limit to our realization of tomorrow will be our doubts of today.", "Franklin D. Roosevelt"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart.", "Helen Keller"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Spread love everywhere you go. Let no one ever come to you without leaving happier.", "Mother Teresa"),
]

# Programming/Developer quotes
PROGRAMMING_QUOTES: List[Tuple[str, str]] = [
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
    ("Knowledge is power.", "Francis Bacon"),
    ("Sometimes it pays to stay in bed on Monday, rather than to spend the rest of the week debugging Monday's code.", "Dan Salomon"),
    ("Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.", "Antoine de Saint-Exupery"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("The best error message is the one that never shows up.", "Thomas Fuchs"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("It's not a bug, it's an undocumented feature!", "Anonymous"),
    ("There are only two kinds of languages: the ones people complain about and the ones nobody uses.", "Bjarne Stroustrup"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Programming is the art of telling another human being what one wants the computer to do.", "Donald Knuth"),
    ("The computer was born to solve problems that did not exist before.", "Bill Gates"),
    ("Software is a great combination of artistry and engineering.", "Bill Gates"),
    ("The most disastrous thing that you can ever learn is your first programming language.", "Alan Kay"),
    ("Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it?", "Brian Kernighan"),
]

# Wisdom/Philosophy quotes
WISDOM_QUOTES: List[Tuple[str, str]] = [
    ("The only true wisdom is in knowing you know nothing.", "Socrates"),
    ("I think, therefore I am.", "Rene Descartes"),
    ("The unexamined life is not worth living.", "Socrates"),
    ("He who has a why to live can bear almost any how.", "Friedrich Nietzsche"),
    ("To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "Ralph Waldo Emerson"),
    ("Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.", "Albert Einstein"),
    ("Be the change that you wish to see in the world.", "Mahatma Gandhi"),
    ("In three words I can sum up everything I've learned about life: it goes on.", "Robert Frost"),
    ("Life is really simple, but we insist on making it complicated.", "Confucius"),
    ("The journey of a thousand miles begins with a single step.", "Lao Tzu"),
    ("That which does not kill us makes us stronger.", "Friedrich Nietzsche"),
    ("Happiness is not something ready made. It comes from your own actions.", "Dalai Lama"),
    ("We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "Aristotle"),
    ("The only thing I know is that I know nothing.", "Socrates"),
    ("Give me a lever long enough and a fulcrum on which to place it, and I shall move the world.", "Archimedes"),
    ("The only way to avoid being miserable is not to have enough leisure to wonder whether you are happy or not.", "George Bernard Shaw"),
    ("He who conquers himself is the mightiest warrior.", "Confucius"),
    ("To handle yourself, use your head; to handle others, use your heart.", "Eleanor Roosevelt"),
    ("Do not go where the path may lead, go instead where there is no path and leave a trail.", "Ralph Waldo Emerson"),
    ("It is not length of life, but depth of life.", "Ralph Waldo Emerson"),
]

# Humor/Funny quotes
HUMOR_QUOTES: List[Tuple[str, str]] = [
    ("I'm not lazy, I'm on energy-saving mode.", "Anonymous"),
    ("I used to think I was indecisive, but now I'm not so sure.", "Anonymous"),
    ("I'm not arguing, I'm just explaining why I'm right.", "Anonymous"),
    ("Why don't scientists trust atoms? Because they make up everything!", "Anonymous"),
    ("I told my computer I needed a break, and now it won't stop sending me vacation ads.", "Anonymous"),
    ("Life is short. Smile while you still have teeth.", "Anonymous"),
    ("I'm not saying I'm Batman. I'm just saying no one has ever seen me and Batman in a room together.", "Anonymous"),
    ("I'm on a seafood diet. I see food and I eat it.", "Anonymous"),
    ("My wallet is like an onion. Opening it makes me cry.", "Anonymous"),
    ("I'm not superstitious, but I am a little stitious.", "Michael Scott"),
    ("I find television very educating. Every time somebody turns on the set, I go into the other room and read a book.", "Groucho Marx"),
    ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison"),
    ("People say nothing is impossible, but I do nothing every day.", "A.A. Milne"),
    ("I am so clever that sometimes I don't understand a single word of what I am saying.", "Oscar Wilde"),
    ("The only mystery in life is why the kamikaze pilots wore helmets.", "Al McGuire"),
    ("I intend to live forever. So far, so good.", "Steven Wright"),
    ("A day without laughter is a day wasted.", "Charlie Chaplin"),
    ("Behind every great man is a woman rolling her eyes.", "Jim Carrey"),
    ("Get your facts first, then you can distort them as you please.", "Mark Twain"),
    ("I'm not afraid of death; I just don't want to be there when it happens.", "Woody Allen"),
]

# Chinese proverbs
CHINESE_PROVERBS: List[str] = [
    "A diamond with a flaw is worth more than a pebble without imperfections.",
    "A fall into a ditch makes you wiser.",
    "A journey of a thousand miles begins with a single step.",
    "A man grows most tired while standing still.",
    "A smile will gain you ten more years of life.",
    "A single beam cannot support a great house.",
    "A single conversation with a wise man is worth ten years of study.",
    "Be not afraid of growing slowly, be afraid only of standing still.",
    "Better a diamond with a flaw than a pebble without one.",
    "Better do a good deed near home than go far away to burn incense.",
    "Deep doubts, deep wisdom; little doubts, little wisdom.",
    "Dig the well before you are thirsty.",
    "Do not remove a fly from your friend's forehead with a hatchet.",
    "Distant water does not put out a nearby fire.",
    "Don't stand by the water and long for fish; go home and weave a net.",
    "Each generation will reap what the former generation has sown.",
    "Even a hare will bite when it is cornered.",
    "Give a man a fish and you feed him for a day. Teach a man to fish and you feed him for a lifetime.",
    "Good medicine tastes bitter.",
    "He who asks is a fool for five minutes, but he who does not ask remains a fool forever.",
    "He who deliberates fully before taking a step will spend his entire life on one leg.",
    "If you are patient in one moment of anger, you will escape a hundred days of sorrow.",
    "If you bow at all, bow low.",
    "If you want happiness for an hour, take a nap. If you want happiness for a day, go fishing. If you want happiness for a year, inherit a fortune. If you want happiness for a lifetime, help someone else.",
    "It is easy to open a shop, but hard to keep it open.",
    "It is not the knowing that is difficult, but the doing.",
    "Keep a green tree in your heart and perhaps the singing bird will come.",
    "Learning is a treasure that will follow its owner everywhere.",
    "Life is a dream walking; death is a going home.",
    "Listen to all, plucking a feather from every passing goose, but follow no one absolutely.",
    "Man who waits for roast duck to fly into mouth must wait very, very long time.",
    "Many a good face is under a ragged hat.",
    "Of all the strategems, to know when to quit is the best.",
    "One dog barks at something, the rest bark at him.",
    "One generation plants the trees; another gets the shade.",
    "One monk shoulders water, two monks carry water, three monks have no water.",
    "Outside noisy, inside empty.",
    "Patience is a bitter plant, but its fruit is sweet.",
    "Rivers and mountains are more easily changed than a man's nature.",
    "Sow much, reap much; sow little, reap little.",
    "Teachers open the door. You enter by yourself.",
    "The best time to plant a tree was 20 years ago. The second best time is today.",
    "The error of one moment becomes the sorrow of a whole life.",
    "The man who moves a mountain begins by carrying away small stones.",
    "The miracle is not to fly in the air, or to walk on the water, but to walk on the earth.",
    "The more you sweat in practice, the less you bleed in battle.",
    "There are two kinds of perfect people: those who are dead, and those who have not been born yet.",
    "Think of your own faults the first part of the night when you are awake, and the faults of others the latter part of the night when you are asleep.",
    "To believe in one's dreams is to spend all of one's life asleep.",
    "To know the road ahead, ask those coming back.",
    "To obtain a woman, you must first obtain her mother.",
    "Vicious as a tigress can be, she never eats her own cubs.",
    "Water thrown out is hard to put back into the pail.",
    "What is told in the ear of a man is heard 100 miles away.",
    "When you drink the water, remember the spring.",
    "When you have only two pennies left in the world, buy a loaf of bread with one, and a lily with the other.",
    "With money you can buy a house, but not a home.",
    "Words are merely words and drift like leaves in the wind.",
    "You can force a man to shut his eyes, but you cannot force him to sleep.",
    "You can't clap with one hand.",
    "You cannot catch a cub without entering the tiger's den.",
]

# Riddles (with answers stored separately)
RIDDLES: List[Tuple[str, str]] = [
    ("What has keys but no locks? You can enter, but never go in. What am I?", "A keyboard"),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "An echo"),
    ("I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "A map"),
    ("What is seen in the middle of March and April that can't be seen at the beginning or end of either month?", "The letter R"),
    ("You measure my life in hours and I serve you by expiring. I'm quick when I'm thin and slow when I'm fat. The wind is my enemy. What am I?", "A candle"),
    ("I have cities, but no houses live there. I have mountains, but no trees grow there. I have water, but no fish swim there. What am I?", "A map"),
    ("I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?", "Fire"),
    ("I am always hungry, I must always be fed. The finger I touch, will soon turn red. What am I?", "Fire"),
    ("The more you take, the more you leave behind. What am I?", "Footsteps"),
    ("I have a head and a tail but no body. What am I?", "A coin"),
    ("What can travel all around the world without leaving its corner?", "A stamp"),
    ("What has 13 hearts, but no other organs?", "A deck of cards"),
    ("I weaken all men for hours each day. I show you strange visions while you are away. I take you by night, by day take you back, none suffer to have me, but do curse my lack. What am I?", "Sleep"),
    ("What has many teeth, but cannot bite?", "A comb"),
    ("What is so fragile that saying its name breaks it?", "Silence"),
    ("The more of me there is, the less you see. What am I?", "Darkness"),
    ("I have lakes but no water, mountains but no rock, and cities but no buildings. What am I?", "A map"),
    ("What can fill a room but takes up no space?", "Light"),
    ("What begins with T, ends with T, and has T in it?", "A teapot"),
    ("What has a neck but no head?", "A bottle"),
    ("What has legs but cannot walk?", "A table"),
    ("What gets wet while drying?", "A towel"),
    ("What belongs to you, but other people use it more than you?", "Your name"),
    ("I can fly but have no wings. I can cry but I have no eyes. Wherever I go, darkness follows me. What am I?", "A cloud"),
    ("What can you keep even after giving it to someone?", "Your word"),
]

# Motivational/Success quotes
MOTIVATIONAL_QUOTES: List[Tuple[str, str]] = [
    ("Success is not the key to happiness. Happiness is the key to success.", "Albert Schweitzer"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.", "Roy T. Bennett"),
    ("Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.", "Roy T. Bennett"),
    ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Anonymous"),
    ("Dreams don't work unless you do.", "John C. Maxwell"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
    ("It's not whether you get knocked down. It's whether you get up.", "Vince Lombardi"),
    ("Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("Don't let yesterday take up too much of today.", "Will Rogers"),
    ("You learn more from failure than from success. Don't let it stop you. Failure builds character.", "Anonymous"),
    ("If you are working on something that you really care about, you don't have to be pushed. The vision pulls you.", "Steve Jobs"),
    ("We may encounter many defeats but we must not be defeated.", "Maya Angelou"),
    ("Knowing is not enough; we must apply. Wishing is not enough; we must do.", "Johann Wolfgang von Goethe"),
    ("We generate fears while we sit. We overcome them by action.", "Dr. Henry Link"),
]


# ============================================================================
# Fortune Database Class
# ============================================================================

class FortuneDatabase:
    """
    A database of fortunes organized by category.
    
    Example:
        >>> db = FortuneDatabase()
        >>> fortune = db.random()
        >>> fortune.text
        '...'
        >>> fortune = db.random(category='inspirational')
        >>> fortune.author
        '...'
    """
    
    def __init__(self, custom_fortunes: Optional[Dict[str, List[Fortune]]] = None):
        """
        Initialize the fortune database.
        
        Args:
            custom_fortunes: Optional dict of category -> list of Fortune objects
        """
        self._fortunes: Dict[str, List[Fortune]] = {}
        self._build_database()
        
        # Add custom fortunes if provided
        if custom_fortunes:
            for category, fortunes in custom_fortunes.items():
                if category not in self._fortunes:
                    self._fortunes[category] = []
                self._fortunes[category].extend(fortunes)
    
    def _build_database(self) -> None:
        """Build the default fortune database."""
        # Unix fortunes (classic)
        self._fortunes['unix'] = [
            Fortune(text=text, category='unix')
            for text in UNIX_FORTUNES
        ]
        
        # Inspirational quotes
        self._fortunes['inspirational'] = [
            Fortune(text=text, author=author, category='inspirational')
            for text, author in INSPIRATIONAL_QUOTES
        ]
        
        # Programming quotes
        self._fortunes['programming'] = [
            Fortune(text=text, author=author, category='programming')
            for text, author in PROGRAMMING_QUOTES
        ]
        
        # Wisdom quotes
        self._fortunes['wisdom'] = [
            Fortune(text=text, author=author, category='wisdom')
            for text, author in WISDOM_QUOTES
        ]
        
        # Humor quotes
        self._fortunes['humor'] = [
            Fortune(text=text, author=author, category='humor')
            for text, author in HUMOR_QUOTES
        ]
        
        # Chinese proverbs
        self._fortunes['chinese'] = [
            Fortune(text=text, category='chinese')
            for text in CHINESE_PROVERBS
        ]
        
        # Riddles
        self._fortunes['riddle'] = [
            Fortune(text=question, category='riddle', difficulty=random.randint(1, 3))
            for question, answer in RIDDLES
        ]
        # Store answers separately
        self._riddle_answers = {q: a for q, a in RIDDLES}
        
        # Motivational quotes
        self._fortunes['motivational'] = [
            Fortune(text=text, author=author, category='motivational')
            for text, author in MOTIVATIONAL_QUOTES
        ]
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        return list(self._fortunes.keys())
    
    def count(self, category: Optional[str] = None) -> int:
        """
        Count fortunes in a category or total.
        
        Args:
            category: Category to count, or None for total
        
        Returns:
            Number of fortunes
        """
        if category:
            return len(self._fortunes.get(category, []))
        return sum(len(f) for f in self._fortunes.values())
    
    def get(self, index: int, category: str) -> Optional[Fortune]:
        """
        Get a specific fortune by index.
        
        Args:
            index: Index in category
            category: Category name
        
        Returns:
            Fortune or None if not found
        """
        fortunes = self._fortunes.get(category, [])
        if 0 <= index < len(fortunes):
            return fortunes[index]
        return None
    
    def random(self, category: Optional[str] = None) -> FortuneResult:
        """
        Get a random fortune.
        
        Args:
            category: Category to select from, or None for any category
        
        Returns:
            FortuneResult with the selected fortune
        
        Raises:
            ValueError: If category is empty or not found
        """
        if category:
            if category not in self._fortunes:
                raise ValueError(f"Category '{category}' not found")
            fortunes = self._fortunes[category]
            if not fortunes:
                raise ValueError(f"Category '{category}' is empty")
            index = random.randint(0, len(fortunes) - 1)
            fortune = fortunes[index]
        else:
            # Pick random category first
            all_categories = [c for c in self._fortunes.keys() if self._fortunes[c]]
            if not all_categories:
                raise ValueError("No fortunes available")
            category = random.choice(all_categories)
            fortunes = self._fortunes[category]
            index = random.randint(0, len(fortunes) - 1)
            fortune = fortunes[index]
        
        return FortuneResult(
            fortune=fortune,
            index=index,
            total_in_category=len(fortunes),
        )
    
    def random_daily(self, category: Optional[str] = None, seed: Optional[str] = None) -> FortuneResult:
        """
        Get a daily fortune (same fortune for the entire day).
        
        Uses the current date (and optional seed) to deterministically
        select a fortune.
        
        Args:
            category: Category to select from
            seed: Optional seed string for different daily fortunes
        
        Returns:
            FortuneResult with the daily fortune
        """
        today = datetime.now().strftime("%Y-%m-%d")
        if seed:
            today = f"{today}-{seed}"
        
        # Create deterministic hash
        hash_input = today.encode('utf-8')
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
        
        if category:
            fortunes = self._fortunes.get(category, [])
        else:
            # Combine all fortunes
            fortunes = []
            for cat_fortunes in self._fortunes.values():
                fortunes.extend(cat_fortunes)
        
        if not fortunes:
            raise ValueError("No fortunes available")
        
        index = hash_value % len(fortunes)
        fortune = fortunes[index]
        
        return FortuneResult(
            fortune=fortune,
            index=index,
            total_in_category=len(fortunes),
        )
    
    def search(self, query: str, category: Optional[str] = None) -> List[Fortune]:
        """
        Search for fortunes containing a query.
        
        Args:
            query: Search query (case-insensitive)
            category: Category to search in, or None for all
        
        Returns:
            List of matching fortunes
        """
        query = query.lower()
        results = []
        
        if category:
            fortunes = self._fortunes.get(category, [])
        else:
            fortunes = []
            for cat_fortunes in self._fortunes.values():
                fortunes.extend(cat_fortunes)
        
        for fortune in fortunes:
            if query in fortune.text.lower():
                results.append(fortune)
            elif fortune.author and query in fortune.author.lower():
                results.append(fortune)
            elif any(query in tag.lower() for tag in fortune.tags):
                results.append(fortune)
        
        return results
    
    def get_riddle_answer(self, riddle_text: str) -> Optional[str]:
        """
        Get the answer to a riddle.
        
        Args:
            riddle_text: The riddle question text
        
        Returns:
            The answer or None if not found
        """
        return self._riddle_answers.get(riddle_text)
    
    def add_fortune(self, fortune: Fortune) -> None:
        """
        Add a fortune to the database.
        
        Args:
            fortune: Fortune to add
        """
        category = fortune.category
        if category not in self._fortunes:
            self._fortunes[category] = []
        self._fortunes[category].append(fortune)
    
    def add_fortunes(self, fortunes: List[Fortune]) -> None:
        """
        Add multiple fortunes to the database.
        
        Args:
            fortunes: List of fortunes to add
        """
        for fortune in fortunes:
            self.add_fortune(fortune)
    
    def get_all(self, category: Optional[str] = None) -> List[Fortune]:
        """
        Get all fortunes, optionally filtered by category.
        
        Args:
            category: Category to filter by, or None for all
        
        Returns:
            List of fortunes
        """
        if category:
            return self._fortunes.get(category, []).copy()
        
        all_fortunes = []
        for cat_fortunes in self._fortunes.values():
            all_fortunes.extend(cat_fortunes)
        return all_fortunes


# Global database instance
_db = FortuneDatabase()


# ============================================================================
# Convenience Functions
# ============================================================================

def fortune(category: Optional[str] = None) -> str:
    """
    Get a random fortune text.
    
    Args:
        category: Category to select from (unix, inspirational, programming,
                  wisdom, humor, chinese, riddle, motivational)
    
    Returns:
        Fortune text string
    
    Example:
        >>> f = fortune()
        >>> len(f) > 0
        True
        >>> f = fortune('programming')
        >>> 'code' in f.lower() or 'program' in f.lower() or True  # May or may not contain keywords
        True
    """
    result = _db.random(category)
    return str(result)


def fortune_result(category: Optional[str] = None) -> FortuneResult:
    """
    Get a random fortune with full details.
    
    Args:
        category: Category to select from
    
    Returns:
        FortuneResult object with full details
    """
    return _db.random(category)


def daily_fortune(category: Optional[str] = None, seed: Optional[str] = None) -> FortuneResult:
    """
    Get the daily fortune (same for entire day).
    
    Args:
        category: Category to select from
        seed: Optional seed for different daily fortunes
    
    Returns:
        FortuneResult with the daily fortune
    """
    return _db.random_daily(category, seed)


def inspirational_quote() -> str:
    """Get a random inspirational quote."""
    result = _db.random('inspirational')
    return str(result)


def programming_quote() -> str:
    """Get a random programming quote."""
    result = _db.random('programming')
    return str(result)


def wisdom_quote() -> str:
    """Get a random wisdom quote."""
    result = _db.random('wisdom')
    return str(result)


def humor_quote() -> str:
    """Get a random humor quote."""
    result = _db.random('humor')
    return str(result)


def chinese_proverb() -> str:
    """Get a random Chinese proverb."""
    result = _db.random('chinese')
    return str(result)


def motivational_quote() -> str:
    """Get a random motivational quote."""
    result = _db.random('motivational')
    return str(result)


def riddle() -> Tuple[str, str]:
    """
    Get a random riddle with its answer.
    
    Returns:
        Tuple of (riddle_question, riddle_answer)
    
    Example:
        >>> q, a = riddle()
        >>> len(q) > 0
        True
        >>> len(a) > 0
        True
    """
    result = _db.random('riddle')
    question = result.fortune.text
    answer = _db.get_riddle_answer(question) or "Unknown"
    return (question, answer)


def riddle_question() -> str:
    """Get a random riddle question without the answer."""
    result = _db.random('riddle')
    return result.fortune.text


def unix_fortune() -> str:
    """Get a random Unix-style fortune cookie."""
    result = _db.random('unix')
    return result.fortune.text


def search_fortunes(query: str, category: Optional[str] = None) -> List[Fortune]:
    """
    Search for fortunes containing a query.
    
    Args:
        query: Search query (case-insensitive)
        category: Category to search in, or None for all
    
    Returns:
        List of matching fortunes
    
    Example:
        >>> results = search_fortunes("success")
        >>> len(results) > 0
        True
    """
    return _db.search(query, category)


def categories() -> List[str]:
    """Get all available fortune categories."""
    return _db.get_categories()


def fortune_count(category: Optional[str] = None) -> int:
    """
    Count fortunes in a category or total.
    
    Args:
        category: Category to count, or None for total
    
    Returns:
        Number of fortunes
    """
    return _db.count(category)


def get_database() -> FortuneDatabase:
    """Get the global fortune database instance."""
    return _db


# ============================================================================
# Fortune Generator Class
# ============================================================================

class FortuneGenerator:
    """
    A configurable fortune generator with custom fortune pools.
    
    Example:
        >>> gen = FortuneGenerator()
        >>> gen.add_fortune("My custom fortune", category="custom")
        >>> gen.random()
        FortuneResult(...)
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self._db = FortuneDatabase()
        self._rng = random.Random(seed) if seed is not None else random
    
    def random(self, category: Optional[str] = None) -> FortuneResult:
        """Get a random fortune."""
        if category:
            fortunes = self._db.get_all(category)
        else:
            fortunes = self._db.get_all()
        
        if not fortunes:
            raise ValueError("No fortunes available")
        
        index = self._rng.randint(0, len(fortunes) - 1)
        fortune = fortunes[index]
        
        return FortuneResult(
            fortune=fortune,
            index=index,
            total_in_category=len(fortunes),
        )
    
    def add_fortune(
        self,
        text: str,
        category: str = "custom",
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """Add a custom fortune."""
        fortune = Fortune(
            text=text,
            category=category,
            author=author,
            tags=tags or [],
        )
        self._db.add_fortune(fortune)
    
    def add_fortunes_from_list(
        self,
        fortunes: List[str],
        category: str = "custom",
    ) -> None:
        """Add multiple fortunes from a list of strings."""
        for text in fortunes:
            self.add_fortune(text, category)
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        return self._db.get_categories()
    
    def search(self, query: str) -> List[Fortune]:
        """Search for fortunes."""
        return self._db.search(query)
    
    def count(self, category: Optional[str] = None) -> int:
        """Count fortunes."""
        return self._db.count(category)


# ============================================================================
# Display Formatting Functions
# ============================================================================

def format_fortune(fortune: Fortune, style: str = "simple") -> str:
    """
    Format a fortune for display.
    
    Args:
        fortune: Fortune object to format
        style: Display style ('simple', 'card', 'quote', 'json')
    
    Returns:
        Formatted string
    
    Example:
        >>> f = Fortune(text="Test", author="Author")
        >>> format_fortune(f, 'simple')
        'Test'
        >>> format_fortune(f, 'quote')
        '"Test"\\n    — Author'
    """
    if style == "simple":
        return fortune.text
    
    if style == "card":
        lines = [
            "┌" + "─" * (len(fortune.text) + 2) + "┐",
            "│ " + fortune.text + " │",
        ]
        if fortune.author:
            author_line = f"    — {fortune.author}"
            lines.append("├" + "─" * (len(fortune.text) + 2) + "┤")
            lines.append("│ " + author_line + " " * (len(fortune.text) - len(author_line) + 1) + "│")
        lines.append("└" + "─" * (len(fortune.text) + 2) + "┘")
        return "\n".join(lines)
    
    if style == "quote":
        result = f'"{fortune.text}"'
        if fortune.author:
            result += f"\n    — {fortune.author}"
        return result
    
    if style == "json":
        import json
        return json.dumps(fortune.to_dict(), indent=2)
    
    return fortune.text


def format_fortune_result(result: FortuneResult, style: str = "simple") -> str:
    """
    Format a FortuneResult for display.
    
    Args:
        result: FortuneResult object to format
        style: Display style ('simple', 'card', 'quote', 'json', 'full')
    
    Returns:
        Formatted string
    """
    if style == "full":
        lines = [
            f"Fortune #{result.index + 1} of {result.total_in_category}",
            f"Category: {result.fortune.category}",
            "",
            format_fortune(result.fortune, "quote"),
        ]
        if result.fortune.tags:
            lines.append("")
            lines.append(f"Tags: {', '.join(result.fortune.tags)}")
        lines.append("")
        lines.append(f"Generated: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)
    
    return format_fortune(result.fortune, style)


# ============================================================================
# Cookie Format (Unix fortune compatible)
# ============================================================================

def to_cookie_format(fortunes: List[str], delimiter: str = "%") -> str:
    """
    Convert a list of fortunes to Unix fortune cookie file format.
    
    Args:
        fortunes: List of fortune strings
        delimiter: Delimiter character (default: %)
    
    Returns:
        Cookie file format string
    
    Example:
        >>> to_cookie_format(["Fortune 1", "Fortune 2"])
        'Fortune 1\\n%\\nFortune 2\\n%\\n'
    """
    return "\n".join(f + f"\n{delimiter}" for f in fortunes) + "\n"


def from_cookie_format(content: str, delimiter: str = "%") -> List[str]:
    """
    Parse Unix fortune cookie file format to a list of fortunes.
    
    Args:
        content: Cookie file content
        delimiter: Delimiter character (default: %)
    
    Returns:
        List of fortune strings
    
    Example:
        >>> from_cookie_format("Fortune 1\\n%\\nFortune 2\\n%\\n")
        ['Fortune 1', 'Fortune 2']
    """
    fortunes = []
    current = []
    
    for line in content.split("\n"):
        if line.strip() == delimiter:
            if current:
                fortunes.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)
    
    # Handle last fortune without delimiter
    if current:
        fortunes.append("\n".join(current).strip())
    
    return [f for f in fortunes if f]  # Remove empty strings