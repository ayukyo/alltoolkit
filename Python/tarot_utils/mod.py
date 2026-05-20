"""
Tarot Card Utilities

A comprehensive tarot card reading and divination toolkit.

Features:
- Complete 78-card tarot deck (22 Major Arcana, 56 Minor Arcana)
- Multiple spread layouts (Celtic Cross, Three Card, Relationship, etc.)
- Card meanings for upright and reversed positions
- Daily draws and random readings
- Detailed interpretations for each card position
- No external dependencies - pure Python implementation
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Tuple, Callable
import random
from datetime import datetime, date
import hashlib


class Arcana(Enum):
    """Tarot card arcana types."""
    MAJOR = "major"
    MINOR = "minor"


class Suit(Enum):
    """Minor Arcana suits."""
    WANDS = "wands"
    CUPS = "cups"
    SWORDS = "swords"
    PENTACLES = "pentacles"


class Orientation(Enum):
    """Card orientation."""
    UPRIGHT = "upright"
    REVERSED = "reversed"


# Major Arcana Cards
MAJOR_ARCANA = {
    0: {
        "name": "The Fool",
        "keywords": ["beginnings", "innocence", "spontaneity", "free spirit"],
        "upright": "New beginnings, fresh start, innocence, spontaneity, leap of faith, unlimited potential. The Fool represents the start of a journey, embracing the unknown with childlike wonder.",
        "reversed": "Recklessness, risk-taking, foolishness, naivety, lack of planning. You may be acting without thinking or ignoring important warnings.",
        "element": "Air",
        "zodiac": "Uranus",
        "theme": "New Beginnings"
    },
    1: {
        "name": "The Magician",
        "keywords": ["manifestation", "resourcefulness", "power", "inspired action"],
        "upright": "Manifestation, resourcefulness, power, inspired action. You have all the tools you need to succeed. Focus your will and take action.",
        "reversed": "Manipulation, poor planning, untapped talents, latent potential. Your skills are being wasted or misused.",
        "element": "Air",
        "zodiac": "Mercury",
        "theme": "Creation"
    },
    2: {
        "name": "The High Priestess",
        "keywords": ["intuition", "sacred knowledge", "divine feminine", "subconscious mind"],
        "upright": "Intuition, sacred knowledge, divine feminine, subconscious mind. Trust your inner voice and the mysteries unfolding within.",
        "reversed": "Secrets, disconnection from intuition, withdrawal, silence. You may be ignoring your inner wisdom or repressing important truths.",
        "element": "Water",
        "zodiac": "Moon",
        "theme": "Mystery"
    },
    3: {
        "name": "The Empress",
        "keywords": ["femininity", "beauty", "nature", "nurturing", "abundance"],
        "upright": "Femininity, beauty, nature, nurturing, abundance. Connect with your sensual side and embrace the natural world around you.",
        "reversed": "Creative block, dependence on others, emptiness, smothering. You may be neglecting your own needs or stifling your creativity.",
        "element": "Earth",
        "zodiac": "Venus",
        "theme": "Nurturing"
    },
    4: {
        "name": "The Emperor",
        "keywords": ["authority", "establishment", "structure", "father figure"],
        "upright": "Authority, establishment, structure, father figure. Step into your power and create order from chaos. Leadership and control.",
        "reversed": "Tyranny, rigidity, coldness, domination. Abuse of power or excessive control. Rebelliousness against authority.",
        "element": "Fire",
        "zodiac": "Aries",
        "theme": "Authority"
    },
    5: {
        "name": "The Hierophant",
        "keywords": ["spiritual wisdom", "religious beliefs", "conformity", "tradition"],
        "upright": "Spiritual wisdom, religious beliefs, conformity, tradition. Seek guidance from established institutions or spiritual teachers.",
        "reversed": "Personal beliefs, freedom, challenging status quo, unconventional approaches. Break free from traditional thinking.",
        "element": "Earth",
        "zodiac": "Taurus",
        "theme": "Tradition"
    },
    6: {
        "name": "The Lovers",
        "keywords": ["love", "harmony", "relationships", "values alignment", "choices"],
        "upright": "Love, harmony, relationships, values alignment, choices. A significant relationship or important decision about your values.",
        "reversed": "Self-love, disharmony, imbalance, misalignment of values. Relationship challenges or difficult choices ahead.",
        "element": "Air",
        "zodiac": "Gemini",
        "theme": "Union"
    },
    7: {
        "name": "The Chariot",
        "keywords": ["control", "willpower", "success", "determination", "action"],
        "upright": "Control, willpower, success, determination, action. Victory through focused effort and determination. Stay on course.",
        "reversed": "Self-discipline, opposition, lack of direction, aggression. Loss of control or being pulled in different directions.",
        "element": "Water",
        "zodiac": "Cancer",
        "theme": "Victory"
    },
    8: {
        "name": "Strength",
        "keywords": ["strength", "courage", "persuasion", "influence", "compassion"],
        "upright": "Strength, courage, persuasion, influence, compassion. Inner strength and gentle power. Face challenges with grace.",
        "reversed": "Inner strength, insecurity, self-doubt, weakness. Lack of confidence or giving in to fear.",
        "element": "Fire",
        "zodiac": "Leo",
        "theme": "Courage"
    },
    9: {
        "name": "The Hermit",
        "keywords": ["soul-searching", "introspection", "inner guidance", "solitude"],
        "upright": "Soul-searching, introspection, inner guidance, solitude. Take time for reflection and seek inner wisdom.",
        "reversed": "Isolation, loneliness, withdrawal, alienation. Excessive withdrawal or fear of connecting with others.",
        "element": "Earth",
        "zodiac": "Virgo",
        "theme": "Reflection"
    },
    10: {
        "name": "Wheel of Fortune",
        "keywords": ["good luck", "karma", "life cycles", "destiny", "turning point"],
        "upright": "Good luck, karma, life cycles, destiny, turning point. Change is coming - embrace the cycles of life.",
        "reversed": "Bad luck, resistance to change, breaking cycles, external forces. Feeling powerless against circumstances.",
        "element": "Fire",
        "zodiac": "Jupiter",
        "theme": "Change"
    },
    11: {
        "name": "Justice",
        "keywords": ["justice", "fairness", "truth", "cause and effect", "law"],
        "upright": "Justice, fairness, truth, cause and effect, law. Balance and impartiality. Accountability for actions.",
        "reversed": "Unfairness, lack of accountability, dishonesty, legal injustice. Injustice or refusing to accept consequences.",
        "element": "Air",
        "zodiac": "Libra",
        "theme": "Balance"
    },
    12: {
        "name": "The Hanged Man",
        "keywords": ["pause", "surrender", "letting go", "new perspectives"],
        "upright": "Pause, surrender, letting go, new perspectives. A time for sacrifice and seeing things differently.",
        "reversed": "Delays, resistance, stalling, indecision. Fighting necessary changes or being stuck in limbo.",
        "element": "Water",
        "zodiac": "Neptune",
        "theme": "Sacrifice"
    },
    13: {
        "name": "Death",
        "keywords": ["endings", "change", "transformation", "transition"],
        "upright": "Endings, change, transformation, transition. Profound change and transformation. Let go of what no longer serves you.",
        "reversed": "Resistance to change, personal transformation, inner purging, fear of change. Clinging to what must end.",
        "element": "Water",
        "zodiac": "Scorpio",
        "theme": "Transformation"
    },
    14: {
        "name": "Temperance",
        "keywords": ["balance", "moderation", "patience", "purpose"],
        "upright": "Balance, moderation, patience, purpose. Find middle ground and practice restraint. Harmony in all things.",
        "reversed": "Imbalance, excess, self-healing, realignment. Lack of long-term vision or extremes in behavior.",
        "element": "Fire",
        "zodiac": "Sagittarius",
        "theme": "Harmony"
    },
    15: {
        "name": "The Devil",
        "keywords": ["shadow self", "attachment", "addiction", "restriction", "sexuality"],
        "upright": "Shadow self, attachment, addiction, restriction, sexuality. Bondage to material concerns or unhealthy attachments.",
        "reversed": "Releasing limiting beliefs, exploring dark thoughts, detachment, breaking free. Liberation from constraints.",
        "element": "Earth",
        "zodiac": "Capricorn",
        "theme": "Bondage"
    },
    16: {
        "name": "The Tower",
        "keywords": ["sudden change", "upheaval", "chaos", "revelation", "awakening"],
        "upright": "Sudden change, upheaval, chaos, revelation, awakening. Dramatic transformation through destruction of the old.",
        "reversed": "Personal transformation, fear of change, averting disaster, delaying the inevitable. Resisting necessary change.",
        "element": "Fire",
        "zodiac": "Mars",
        "theme": "Upheaval"
    },
    17: {
        "name": "The Star",
        "keywords": ["hope", "faith", "purpose", "renewal", "spirituality"],
        "upright": "Hope, faith, purpose, renewal, spirituality. Calm after the storm. Trust in the universe and your path.",
        "reversed": "Lack of faith, despair, self-trust, disconnection. Loss of hope or feeling disconnected from spirit.",
        "element": "Air",
        "zodiac": "Aquarius",
        "theme": "Hope"
    },
    18: {
        "name": "The Moon",
        "keywords": ["illusion", "fear", "anxiety", "subconscious", "intuition"],
        "upright": "Illusion, fear, anxiety, subconscious, intuition. Things are not as they seem. Navigate through confusion and trust instincts.",
        "reversed": "Release of fear, repressed emotions, inner confusion. Facing fears or releasing repressed emotions.",
        "element": "Water",
        "zodiac": "Pisces",
        "theme": "Mystery"
    },
    19: {
        "name": "The Sun",
        "keywords": ["positivity", "fun", "warmth", "success", "vitality"],
        "upright": "Positivity, fun, warmth, success, vitality. Joy, success, and celebration. Everything is illuminated.",
        "reversed": "Inner child, feeling down, overly optimistic, temporary depression. Inner blockages to happiness.",
        "element": "Fire",
        "zodiac": "Sun",
        "theme": "Joy"
    },
    20: {
        "name": "Judgement",
        "keywords": ["judgement", "rebirth", "inner calling", "absolution"],
        "upright": "Judgement, rebirth, inner calling, absolution. A time of reflection and awakening. Answer your higher calling.",
        "reversed": "Self-doubt, inner critic, ignoring the call, excessive self-analysis. Refusing to face truths or make decisions.",
        "element": "Fire",
        "zodiac": "Pluto",
        "theme": "Awakening"
    },
    21: {
        "name": "The World",
        "keywords": ["completion", "integration", "accomplishment", "travel"],
        "upright": "Completion, integration, accomplishment, travel. Fulfillment and achievement. The end of a cycle.",
        "reversed": "Seeking personal closure, short-cuts, delays, lack of closure. Incomplete tasks or seeking shortcuts.",
        "element": "Earth",
        "zodiac": "Saturn",
        "theme": "Completion"
    }
}

# Minor Arcana - Court Cards and Number Cards
MINOR_ARCANA_COURT = {
    "wands": {
        "king": {
            "name": "King of Wands",
            "keywords": ["leadership", "vision", "entrepreneur", "honor"],
            "upright": "Natural leader, vision, entrepreneur, honor. Take charge with confidence and inspire others.",
            "reversed": "Tyranny, arrogance, impulsiveness, expectations unmet. Overbearing leadership or abuse of power."
        },
        "queen": {
            "name": "Queen of Wands",
            "keywords": ["confidence", "independence", "social", "determined"],
            "upright": "Confidence, independence, social, determined. Charismatic and energetic leadership.",
            "reversed": "Selfishness, jealousy, bitterness, unfaithful. Overconfidence turning into arrogance."
        },
        "knight": {
            "name": "Knight of Wands",
            "keywords": ["action", "adventure", "impulsiveness", "fearless"],
            "upright": "Action, adventure, impulsiveness, fearless. Energetic pursuit of goals. Charge ahead!",
            "reversed": "Restlessness, delays, frustration, setbacks. Hasty action leading to problems."
        },
        "page": {
            "name": "Page of Wands",
            "keywords": ["exploration", "excitement", "freedom", "messenger"],
            "upright": "Exploration, excitement, freedom, messenger. New beginnings and creative inspiration.",
            "reversed": "Lack of direction, procrastination, all talk no action. Unfulfilled potential or scattered energy."
        }
    },
    "cups": {
        "king": {
            "name": "King of Cups",
            "keywords": ["emotional balance", "compassion", "diplomatic"],
            "upright": "Emotional balance, compassion, diplomatic. Mastery over emotions and wisdom in relationships.",
            "reversed": "Emotional manipulation, moodiness, coldness. Repressed emotions or emotional manipulation."
        },
        "queen": {
            "name": "Queen of Cups",
            "keywords": ["compassion", "care", "emotional security", "intuitive"],
            "upright": "Compassion, care, emotional security, intuitive. Deep emotional understanding and nurturing.",
            "reversed": "Martyrdom, insecurity, dependency, unrealistic. Emotional dependence or over-sensitivity."
        },
        "knight": {
            "name": "Knight of Cups",
            "keywords": ["romance", "charm", "imagination", "beauty"],
            "upright": "Romance, charm, imagination, beauty. Following your heart and pursuing dreams.",
            "reversed": "Unrealistic, jealousy, moodiness, disappointment. Disillusionment or unrealistic expectations."
        },
        "page": {
            "name": "Page of Cups",
            "keywords": ["creative opportunities", "intuitive", "messenger", "curiosity"],
            "upright": "Creative opportunities, intuitive, messenger, curiosity. New emotional experiences or creative messages.",
            "reversed": "Creative blocks, emotional immaturity, escapism. Avoiding emotional growth."
        }
    },
    "swords": {
        "king": {
            "name": "King of Swords",
            "keywords": ["authority", "truth", "intellect", "clarity"],
            "upright": "Authority, truth, intellect, clarity. Wise leadership through logic and fairness.",
            "reversed": "Manipulation, tyranny, cruelty, lack of compassion. Abuse of power or cruel logic."
        },
        "queen": {
            "name": "Queen of Swords",
            "keywords": ["independence", "clarity", "direct communication", "justice"],
            "upright": "Independence, clarity, direct communication, justice. Sharp mind and honest judgment.",
            "reversed": "Coldness, cruelty, bitterness, judgmental. Overly harsh or emotionally cut off."
        },
        "knight": {
            "name": "Knight of Swords",
            "keywords": ["action", "ambition", "assertiveness", "fearless"],
            "upright": "Action, ambition, assertiveness, fearless. Charge forward with determination and speed.",
            "reversed": "No direction, ruthless, burnout, lack of planning. Reckless action without thought."
        },
        "page": {
            "name": "Page of Swords",
            "keywords": ["curiosity", "restlessness", "new ideas", "messenger"],
            "upright": "Curiosity, restlessness, new ideas, messenger. Mental agility and new perspectives.",
            "reversed": "All talk no action, lack of planning, gossip, avoidance. Scattered thoughts or avoiding truth."
        }
    },
    "pentacles": {
        "king": {
            "name": "King of Pentacles",
            "keywords": ["wealth", "business", "leadership", "security"],
            "upright": "Wealth, business, leadership, security. Financial success and responsible management.",
            "reversed": "Greed, indulgence, sensory, stubbornness. Materialism or poor financial judgment."
        },
        "queen": {
            "name": "Queen of Pentacles",
            "keywords": ["practical", "nurturing", "financially secure", "grounded"],
            "upright": "Practical, nurturing, financially secure, grounded. Balancing material success with care for others.",
            "reversed": "Self-centered, jealousy, workaholic, neglect. Over-focus on material security."
        },
        "knight": {
            "name": "Knight of Pentacles",
            "keywords": ["efficiency", "routine", "conservatism", "methodical"],
            "upright": "Efficiency, routine, conservatism, methodical. Steady progress through disciplined effort.",
            "reversed": "Procrastination, obsessiveness, dullness, laziness. Stagnation or resistance to change."
        },
        "page": {
            "name": "Page of Pentacles",
            "keywords": ["ambitious", "diligent", "new financial opportunities", "messenger"],
            "upright": "Ambitious, diligent, new financial opportunities, messenger. Beginning of material success.",
            "reversed": "Procrastination, lack of progress, poor planning. Unfulfilled potential or lack of focus."
        }
    }
}

# Minor Arcana - Number Cards meanings (1-10)
MINOR_ARCANA_NUMBERS = {
    "wands": {
        1: {"name": "Ace of Wands", "keywords": ["inspiration", "new beginnings", "creative spark"], "upright": "Insppiration, new opportunities, creative potential. A spark of new energy.", "reversed": "Lack of inspiration, delays, false starts. Blocked creative energy."},
        2: {"name": "Two of Wands", "keywords": ["planning", "decisions", "discovery"], "upright": "Planning, making decisions, leaving comfort zone. Future vision and choices.", "reversed": "Fear of unknown, poor planning, lack of direction. Staying in your comfort zone."},
        3: {"name": "Three of Wands", "keywords": ["expansion", "foresight", "progress"], "upright": "Expansion, foresight, progress. Looking ahead to new horizons.", "reversed": "Delays, frustration, lack of foresight. Obstacles to growth."},
        4: {"name": "Four of Wands", "keywords": ["celebration", "harmony", "homecoming"], "upright": "Celebration, harmony, homecoming. Joy and community support.", "reversed": "Lack of harmony, transition, unsettled. Disrupted celebrations."},
        5: {"name": "Five of Wands", "keywords": ["competition", "conflict", "tension"], "upright": "Competition, conflict, tension. Challenges and testing your position.", "reversed": "Conflict resolution, avoiding conflict, inner conflict. Peace after struggle."},
        6: {"name": "Six of Wands", "keywords": ["victory", "public recognition", "success"], "upright": "Victory, public recognition, success. Triumph and being celebrated.", "reversed": "Lack of recognition, fall from grace, self-doubt. Temporary failure."},
        7: {"name": "Seven of Wands", "keywords": ["defiance", "conviction", "holding your ground"], "upright": "Defiance, conviction, holding your ground. Standing up for beliefs.", "reversed": "Giving up, overwhelmed, backing down. Feeling defeated."},
        8: {"name": "Eight of Wands", "keywords": ["speed", "movement", "swift action"], "upright": "Speed, movement, swift action. Things moving quickly forward.", "reversed": "Delays, frustration, waiting. Blocked progress."},
        9: {"name": "Nine of Wands", "keywords": ["resilience", "persistence", "last stand"], "upright": "Resilience, persistence, last stand. Keep going despite challenges.", "reversed": "Exhaustion, giving up, paranoia. Running out of energy."},
        10: {"name": "Ten of Wands", "keywords": ["burden", "responsibility", "hard work"], "upright": "Burden, responsibility, hard work. Carrying a heavy load.", "reversed": "Releasing burden, delegation, collapse. Setting down your load."}
    },
    "cups": {
        1: {"name": "Ace of Cups", "keywords": ["love", "new relationships", "compassion", "creativity"], "upright": "New love, emotional awakening, creativity. An overflow of feelings.", "reversed": "Emotional loss, blocked creativity, emptiness. Repressed emotions."},
        2: {"name": "Two of Cups", "keywords": ["unity", "partnership", "connection"], "upright": "Unity, partnership, connection. A strong bond forming.", "reversed": "Imbalance, broken communication, tension. Disconnection in relationships."},
        3: {"name": "Three of Cups", "keywords": ["celebration", "friendship", "community"], "upright": "Celebration, friendship, community. Joy with others.", "reversed": "Overindulgence, gossip, isolation. Exclusion or excessive partying."},
        4: {"name": "Four of Cups", "keywords": ["contemplation", "apathy", "disconnection"], "upright": "Contemplation, apathy, disconnection. Ignoring opportunities.", "reversed": "New opportunities, engagement, awareness. Breaking from stagnation."},
        5: {"name": "Five of Cups", "keywords": ["loss", "grief", "regret"], "upright": "Loss, grief, regret. Focusing on what was lost.", "reversed": "Recovery, acceptance, moving on. Finding peace after loss."},
        6: {"name": "Six of Cups", "keywords": ["nostalgia", "childhood", "innocence"], "upright": "Nostalgia, childhood memories, innocence. Looking back fondly.", "reversed": "Living in the past, moving forward, childhood issues. Stuck in memories."},
        7: {"name": "Seven of Cups", "keywords": ["choices", "wishful thinking", "illusion"], "upright": "Choices, wishful thinking, illusion. Many options, some deceptive.", "reversed": "Escapism, confusion, overwhelmed. Clearing away illusions."},
        8: {"name": "Eight of Cups", "keywords": ["departure", "disillusionment", "seeking"], "upright": "Departure, disillusionment, seeking higher meaning. Walking away.", "reversed": "Fear of unknown, staying put, aimless wandering. Avoiding needed departure."},
        9: {"name": "Nine of Cups", "keywords": ["satisfaction", "wishes fulfilled", "contentment"], "upright": "Satisfaction, wishes fulfilled, contentment. Emotional fulfillment.", "reversed": "Overindulgence, greed, unfulfilled desires. Unrealistic expectations."},
        10: {"name": "Ten of Cups", "keywords": ["harmony", "marriage", "alignment"], "upright": "Harmony, marriage, alignment. Emotional completion.", "reversed": "Broken family, misalignment, divorce. Disrupted domestic harmony."}
    },
    "swords": {
        1: {"name": "Ace of Swords", "keywords": ["breakthrough", "clarity", "new ideas"], "upright": "Breakthrough, clarity, new ideas. Mental sharpness and truth.", "reversed": "Confusion, lack of clarity, harshness. Blocked mental energy."},
        2: {"name": "Two of Swords", "keywords": ["indecision", "stalemate", "blocked emotions"], "upright": "Indecision, stalemate, blocked emotions. A difficult choice.", "reversed": "Decision made, information revealed, release. Ending the stalemate."},
        3: {"name": "Three of Swords", "keywords": ["heartbreak", "sorrow", "painful truth"], "upright": "Heartbreak, sorrow, painful truth. Deep emotional pain.", "reversed": "Recovery, forgiveness, moving on. Healing from heartbreak."},
        4: {"name": "Four of Swords", "keywords": ["rest", "restoration", "contemplation"], "upright": "Rest, restoration, contemplation. Taking a needed break.", "reversed": "Exhaustion, burnout, restless. Unresolved stress."},
        5: {"name": "Five of Swords", "keywords": ["conflict", "tension", "defeat"], "upright": "Conflict, tension, defeat. Hollow victory or loss.", "reversed": "Reconciliation, moving past conflict, forgiveness. Ending conflict."},
        6: {"name": "Six of Swords", "keywords": ["transition", "change", "journey"], "upright": "Transition, change, journey. Moving toward calmer waters.", "reversed": "Personal transition, resistance to change. Stuck in turbulent waters."},
        7: {"name": "Seven of Swords", "keywords": ["deception", "strategy", "stealth"], "upright": "Deception, strategy, stealth. Hidden actions or betrayal.", "reversed": "Coming clean, conscience, mental challenges. Revealing the truth."},
        8: {"name": "Eight of Swords", "keywords": ["imprisonment", "entrapment", "self-victimization"], "upright": "Imprisonment, entrapment, self-victimization. Feeling trapped.", "reversed": "Self-liberation, new perspective, empowerment. Breaking free."},
        9: {"name": "Nine of Swords", "keywords": ["anxiety", "fear", "nightmares"], "upright": "Anxiety, fear, nightmares. Overwhelming worry.", "reversed": "Hopelessness, releasing fear, inner turmoil. Working through fears."},
        10: {"name": "Ten of Swords", "keywords": ["painful endings", "betrayal", "loss"], "upright": "Painful endings, betrayal, loss. Rock bottom reached.", "reversed": "Recovery, renewal, resistance. Rising from defeat."}
    },
    "pentacles": {
        1: {"name": "Ace of Pentacles", "keywords": ["opportunity", "prosperity", "new venture"], "upright": "Opportunity, prosperity, new venture. Material and financial potential.", "reversed": "Lost opportunity, lack of planning, poor investment. Missed chances."},
        2: {"name": "Two of Pentacles", "keywords": ["balance", "adaptability", "time management"], "upright": "Balance, adaptability, juggling priorities. Flexible management.", "reversed": "Overwhelm, disorganization, financial issues. Losing balance."},
        3: {"name": "Three of Pentacles", "keywords": ["teamwork", "collaboration", "building"], "upright": "Teamwork, collaboration, skill development. Working together well.", "reversed": "Lack of teamwork, poor execution, working alone. Collaboration issues."},
        4: {"name": "Four of Pentacles", "keywords": ["security", "stability", "control"], "upright": "Security, stability, control. Holding tightly to resources.", "reversed": "Overspending, greed, self-protection. Releasing attachment."},
        5: {"name": "Five of Pentacles", "keywords": ["hardship", "poverty", "isolation"], "upright": "Hardship, poverty, isolation. Material struggle.", "reversed": "Recovery, spiritual poverty, charity. Finding help."},
        6: {"name": "Six of Pentacles", "keywords": ["generosity", "charity", "sharing"], "upright": "Generosity, charity, sharing wealth. Giving and receiving.", "reversed": "One-sided charity, strings attached, debt. Unfair exchange."},
        7: {"name": "Seven of Pentacles", "keywords": ["patience", "investment", "reward"], "upright": "Patience, investment, waiting for results. Long-term vision.", "reversed": "Lack of patience, limited success, poor investment. Frustration."},
        8: {"name": "Eight of Pentacles", "keywords": ["skill development", "craftsmanship", "diligence"], "upright": "Skill development, craftsmanship, diligence. Dedicated work.", "reversed": "Perfectionism, lack of focus, shortcuts. Cutting corners."},
        9: {"name": "Nine of Pentacles", "keywords": ["luxury", "self-sufficiency", "accomplishment"], "upright": "Luxury, self-sufficiency, accomplishment. Enjoying the fruits of labor.", "reversed": "Overwork, show-off, false success. Materialism without fulfillment."},
        10: {"name": "Ten of Pentacles", "keywords": ["legacy", "inheritance", "family"], "upright": "Legacy, inheritance, family wealth. Long-lasting success.", "reversed": "Family conflict, financial failure, losing everything. Generational issues."}
    }
}


@dataclass
class TarotCard:
    """Represents a single tarot card."""
    name: str
    arcana: Arcana
    suit: Optional[Suit] = None
    number: Optional[int] = None
    rank: Optional[str] = None  # For court cards: king, queen, knight, page
    keywords: List[str] = field(default_factory=list)
    upright_meaning: str = ""
    reversed_meaning: str = ""
    element: str = ""
    zodiac: str = ""
    theme: str = ""
    
    def get_meaning(self, orientation: Orientation = Orientation.UPRIGHT) -> str:
        """Get card meaning based on orientation."""
        return self.upright_meaning if orientation == Orientation.UPRIGHT else self.reversed_meaning
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'arcana': self.arcana.value,
            'suit': self.suit.value if self.suit else None,
            'number': self.number,
            'rank': self.rank,
            'keywords': self.keywords,
            'upright_meaning': self.upright_meaning,
            'reversed_meaning': self.reversed_meaning,
            'element': self.element,
            'zodiac': self.zodiac,
            'theme': self.theme
        }


class TarotDeck:
    """Complete 78-card tarot deck."""
    
    def __init__(self):
        self.cards: List[TarotCard] = []
        self._create_deck()
    
    def _create_deck(self):
        """Create all 78 cards."""
        # Major Arcana
        for number, data in MAJOR_ARCANA.items():
            card = TarotCard(
                name=data['name'],
                arcana=Arcana.MAJOR,
                number=number,
                keywords=data['keywords'],
                upright_meaning=data['upright'],
                reversed_meaning=data['reversed'],
                element=data.get('element', ''),
                zodiac=data.get('zodiac', ''),
                theme=data.get('theme', '')
            )
            self.cards.append(card)
        
        # Minor Arcana
        for suit_name in ['wands', 'cups', 'swords', 'pentacles']:
            suit = Suit(suit_name)
            
            # Number cards (Ace-10)
            for number in range(1, 11):
                data = MINOR_ARCANA_NUMBERS[suit_name][number]
                card = TarotCard(
                    name=data['name'],
                    arcana=Arcana.MINOR,
                    suit=suit,
                    number=number,
                    keywords=data['keywords'],
                    upright_meaning=data['upright'],
                    reversed_meaning=data['reversed'],
                    element=self._suit_to_element(suit)
                )
                self.cards.append(card)
            
            # Court cards
            for rank in ['page', 'knight', 'queen', 'king']:
                data = MINOR_ARCANA_COURT[suit_name][rank]
                card = TarotCard(
                    name=data['name'],
                    arcana=Arcana.MINOR,
                    suit=suit,
                    rank=rank,
                    keywords=data['keywords'],
                    upright_meaning=data['upright'],
                    reversed_meaning=data['reversed'],
                    element=self._suit_to_element(suit)
                )
                self.cards.append(card)
    
    @staticmethod
    def _suit_to_element(suit: Suit) -> str:
        """Convert suit to element."""
        mapping = {
            Suit.WANDS: "Fire",
            Suit.CUPS: "Water",
            Suit.SWORDS: "Air",
            Suit.PENTACLES: "Earth"
        }
        return mapping.get(suit, "")
    
    def get_card(self, name: str) -> Optional[TarotCard]:
        """Get a card by name."""
        for card in self.cards:
            if card.name.lower() == name.lower():
                return card
        return None
    
    def get_major_arcana(self) -> List[TarotCard]:
        """Get all Major Arcana cards."""
        return [c for c in self.cards if c.arcana == Arcana.MAJOR]
    
    def get_minor_arcana(self) -> List[TarotCard]:
        """Get all Minor Arcana cards."""
        return [c for c in self.cards if c.arcana == Arcana.MINOR]
    
    def get_by_suit(self, suit: Suit) -> List[TarotCard]:
        """Get all cards of a suit."""
        return [c for c in self.cards if c.suit == suit]
    
    def get_court_cards(self) -> List[TarotCard]:
        """Get all court cards."""
        return [c for c in self.cards if c.rank is not None]


class SpreadType(Enum):
    """Types of tarot spreads."""
    ONE_CARD = "one_card"
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"
    RELATIONSHIP = "relationship"
    DECISION = "decision"
    DAILY = "daily"
    HORSESHOE = "horseshoe"
    MONTHLY = "monthly"


@dataclass
class SpreadPosition:
    """Represents a position in a spread."""
    position: int
    name: str
    description: str
    card: Optional[TarotCard] = None
    orientation: Optional[Orientation] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'position': self.position,
            'name': self.name,
            'description': self.description,
            'card': self.card.to_dict() if self.card else None,
            'card_name': self.card.name if self.card else None,
            'orientation': self.orientation.value if self.orientation else None,
            'meaning': self.card.get_meaning(self.orientation) if self.card and self.orientation else None
        }


# Spread definitions
SPREAD_DEFINITIONS = {
    SpreadType.ONE_CARD: {
        "name": "One Card Draw",
        "positions": [
            {"name": "Guidance", "description": "A single card to guide your day or question"}
        ]
    },
    SpreadType.THREE_CARD: {
        "name": "Three Card Spread",
        "positions": [
            {"name": "Past", "description": "Past influences on your situation"},
            {"name": "Present", "description": "Current situation and energies"},
            {"name": "Future", "description": "Potential outcome or direction"}
        ]
    },
    SpreadType.CELTIC_CROSS: {
        "name": "Celtic Cross",
        "positions": [
            {"name": "Present", "description": "Your current situation"},
            {"name": "Challenge", "description": "The challenge or obstacle you face"},
            {"name": "Foundation", "description": "The root cause or basis of the situation"},
            {"name": "Recent Past", "description": "Recent events influencing the situation"},
            {"name": "Possible Future", "description": "A possible outcome if things continue"},
            {"name": "Near Future", "description": "What will happen soon"},
            {"name": "Your Influence", "description": "Your attitude and influence on the matter"},
            {"name": "External Influence", "description": "Outside forces affecting the situation"},
            {"name": "Hopes and Fears", "description": "Your hopes and fears about the outcome"},
            {"name": "Final Outcome", "description": "The most likely result"}
        ]
    },
    SpreadType.RELATIONSHIP: {
        "name": "Relationship Spread",
        "positions": [
            {"name": "You", "description": "Your position in the relationship"},
            {"name": "Partner", "description": "Your partner's position"},
            {"name": "Connection", "description": "What connects you"},
            {"name": "Strengths", "description": "Relationship strengths"},
            {"name": "Challenges", "description": "Relationship challenges"},
            {"name": "Future", "description": "Where the relationship is heading"}
        ]
    },
    SpreadType.DECISION: {
        "name": "Decision Spread",
        "positions": [
            {"name": "Current Situation", "description": "Where you are now"},
            {"name": "Option A", "description": "The first choice and its outcome"},
            {"name": "Option B", "description": "The second choice and its outcome"},
            {"name": "Hidden Factors", "description": "What you're not seeing"},
            {"name": "Advice", "description": "Guidance for your decision"}
        ]
    },
    SpreadType.DAILY: {
        "name": "Daily Guidance",
        "positions": [
            {"name": "Morning", "description": "Energy for the morning"},
            {"name": "Afternoon", "description": "Energy for the afternoon"},
            {"name": "Evening", "description": "Energy for the evening"},
            {"name": "Focus", "description": "What to focus on today"},
            {"name": "Warning", "description": "What to be aware of"},
            {"name": "Blessing", "description": "A gift or opportunity today"}
        ]
    },
    SpreadType.HORSESHOE: {
        "name": "Horseshoe Spread",
        "positions": [
            {"name": "Past", "description": "Past influences"},
            {"name": "Present", "description": "Current situation"},
            {"name": "Hidden Influences", "description": "What you're not aware of"},
            {"name": "Obstacles", "description": "Challenges ahead"},
            {"name": "External Influences", "description": "Outside forces"},
            {"name": "Near Future", "description": "What's coming soon"},
            {"name": "Outcome", "description": "Likely result"}
        ]
    },
    SpreadType.MONTHLY: {
        "name": "Monthly Spread",
        "positions": [
            {"name": "Overall Theme", "description": "The month's main energy"},
            {"name": "Week 1", "description": "First week focus"},
            {"name": "Week 2", "description": "Second week focus"},
            {"name": "Week 3", "description": "Third week focus"},
            {"name": "Week 4", "description": "Fourth week focus"},
            {"name": "Opportunity", "description": "A key opportunity this month"},
            {"name": "Challenge", "description": "A challenge to overcome"},
            {"name": "Advice", "description": "Guidance for the month"}
        ]
    }
}


@dataclass
class TarotReading:
    """Represents a complete tarot reading."""
    spread_type: SpreadType
    positions: List[SpreadPosition] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    question: Optional[str] = None
    
    def get_summary(self) -> str:
        """Get a summary of the reading."""
        spread_def = SPREAD_DEFINITIONS.get(self.spread_type, {})
        spread_name = spread_def.get('name', self.spread_type.value)
        
        summary = f"=== {spread_name} ===\n"
        summary += f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
        if self.question:
            summary += f"Question: {self.question}\n"
        summary += "\n"
        
        for pos in self.positions:
            if pos.card:
                orientation = "(Reversed)" if pos.orientation == Orientation.REVERSED else "(Upright)"
                summary += f"{pos.position}. {pos.name}: {pos.card.name} {orientation}\n"
                summary += f"   Meaning: {pos.card.get_meaning(pos.orientation)}\n\n"
        
        return summary
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'spread_type': self.spread_type.value,
            'spread_name': SPREAD_DEFINITIONS.get(self.spread_type, {}).get('name', ''),
            'positions': [p.to_dict() for p in self.positions],
            'timestamp': self.timestamp.isoformat(),
            'question': self.question
        }


class TarotReader:
    """Main class for performing tarot readings."""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the tarot reader.
        
        Args:
            seed: Optional random seed for reproducible readings
        """
        self.deck = TarotDeck()
        self.seed = seed
        if seed is not None:
            random.seed(seed)
    
    def draw_card(self, include_reversed: bool = True) -> Tuple[TarotCard, Orientation]:
        """
        Draw a single random card.
        
        Returns:
            Tuple of (card, orientation)
        """
        card = random.choice(self.deck.cards)
        
        if include_reversed:
            orientation = random.choice([Orientation.UPRIGHT, Orientation.REVERSED])
        else:
            orientation = Orientation.UPRIGHT
        
        return card, orientation
    
    def draw_cards(self, count: int, include_reversed: bool = True) -> List[Tuple[TarotCard, Orientation]]:
        """
        Draw multiple random cards.
        
        Args:
            count: Number of cards to draw
            include_reversed: Whether to include reversed cards
        
        Returns:
            List of (card, orientation) tuples
        """
        cards = random.sample(self.deck.cards, min(count, len(self.deck.cards)))
        results = []
        
        for card in cards:
            if include_reversed:
                orientation = random.choice([Orientation.UPRIGHT, Orientation.REVERSED])
            else:
                orientation = Orientation.UPRIGHT
            results.append((card, orientation))
        
        return results
    
    def one_card_reading(self, question: Optional[str] = None, 
                        include_reversed: bool = True) -> TarotReading:
        """
        Perform a one-card reading.
        
        Args:
            question: Optional question for the reading
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        card, orientation = self.draw_card(include_reversed)
        
        position = SpreadPosition(
            position=1,
            name="Guidance",
            description="A single card to guide your day or question",
            card=card,
            orientation=orientation
        )
        
        return TarotReading(
            spread_type=SpreadType.ONE_CARD,
            positions=[position],
            question=question
        )
    
    def three_card_reading(self, 
                          positions: Optional[List[str]] = None,
                          question: Optional[str] = None,
                          include_reversed: bool = True) -> TarotReading:
        """
        Perform a three-card reading.
        
        Args:
            positions: Custom position names (default: Past, Present, Future)
            question: Optional question
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        if positions is None:
            positions = ["Past", "Present", "Future"]
        
        cards = self.draw_cards(3, include_reversed)
        spread_positions = []
        
        default_descriptions = {
            "Past": "Past influences on your situation",
            "Present": "Current situation and energies",
            "Future": "Potential outcome or direction"
        }
        
        for i, (card, orientation) in enumerate(cards):
            pos_name = positions[i] if i < len(positions) else f"Position {i+1}"
            desc = default_descriptions.get(pos_name, f"Position {i+1} in the spread")
            
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_name,
                description=desc,
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.THREE_CARD,
            positions=spread_positions,
            question=question
        )
    
    def celtic_cross_reading(self, question: Optional[str] = None,
                            include_reversed: bool = True) -> TarotReading:
        """
        Perform a Celtic Cross reading.
        
        Args:
            question: Optional question for the reading
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        cards = self.draw_cards(10, include_reversed)
        positions_data = SPREAD_DEFINITIONS[SpreadType.CELTIC_CROSS]['positions']
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.CELTIC_CROSS,
            positions=spread_positions,
            question=question
        )
    
    def relationship_reading(self, question: Optional[str] = None,
                            include_reversed: bool = True) -> TarotReading:
        """
        Perform a relationship spread reading.
        
        Args:
            question: Optional question
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        cards = self.draw_cards(6, include_reversed)
        positions_data = SPREAD_DEFINITIONS[SpreadType.RELATIONSHIP]['positions']
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.RELATIONSHIP,
            positions=spread_positions,
            question=question
        )
    
    def decision_reading(self, question: Optional[str] = None,
                        include_reversed: bool = True) -> TarotReading:
        """
        Perform a decision spread reading.
        
        Args:
            question: Optional question about the decision
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        cards = self.draw_cards(5, include_reversed)
        positions_data = SPREAD_DEFINITIONS[SpreadType.DECISION]['positions']
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.DECISION,
            positions=spread_positions,
            question=question
        )
    
    def daily_reading(self, include_reversed: bool = True) -> TarotReading:
        """
        Perform a daily guidance reading.
        
        Args:
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        cards = self.draw_cards(6, include_reversed)
        positions_data = SPREAD_DEFINITIONS[SpreadType.DAILY]['positions']
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.DAILY,
            positions=spread_positions
        )
    
    def horseshoe_reading(self, question: Optional[str] = None,
                         include_reversed: bool = True) -> TarotReading:
        """
        Perform a horseshoe spread reading.
        
        Args:
            question: Optional question
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        cards = self.draw_cards(7, include_reversed)
        positions_data = SPREAD_DEFINITIONS[SpreadType.HORSESHOE]['positions']
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.HORSESHOE,
            positions=spread_positions,
            question=question
        )
    
    def monthly_reading(self, include_reversed: bool = True) -> TarotReading:
        """
        Perform a monthly spread reading.
        
        Args:
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        cards = self.draw_cards(8, include_reversed)
        positions_data = SPREAD_DEFINITIONS[SpreadType.MONTHLY]['positions']
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=SpreadType.MONTHLY,
            positions=spread_positions
        )
    
    def custom_reading(self, spread_type: SpreadType, 
                      question: Optional[str] = None,
                      include_reversed: bool = True) -> TarotReading:
        """
        Perform a reading of any spread type.
        
        Args:
            spread_type: Type of spread to perform
            question: Optional question
            include_reversed: Whether to include reversed cards
        
        Returns:
            TarotReading object
        """
        positions_data = SPREAD_DEFINITIONS.get(spread_type, {}).get('positions', [])
        if not positions_data:
            raise ValueError(f"Unknown spread type: {spread_type}")
        
        cards = self.draw_cards(len(positions_data), include_reversed)
        
        spread_positions = []
        for i, (card, orientation) in enumerate(cards):
            pos_data = positions_data[i]
            spread_positions.append(SpreadPosition(
                position=i + 1,
                name=pos_data['name'],
                description=pos_data['description'],
                card=card,
                orientation=orientation
            ))
        
        return TarotReading(
            spread_type=spread_type,
            positions=spread_positions,
            question=question
        )


# Convenience functions
def get_card_by_name(name: str) -> Optional[TarotCard]:
    """Get a card by name from the default deck."""
    deck = TarotDeck()
    return deck.get_card(name)


def get_card_meaning(name: str, reversed: bool = False) -> Optional[str]:
    """
    Get the meaning of a card by name.
    
    Args:
        name: Card name
        reversed: Whether to get reversed meaning
    
    Returns:
        Card meaning or None if not found
    """
    card = get_card_by_name(name)
    if card:
        orientation = Orientation.REVERSED if reversed else Orientation.UPRIGHT
        return card.get_meaning(orientation)
    return None


def daily_card(seed: Optional[int] = None) -> Tuple[TarotCard, Orientation]:
    """
    Get a daily card based on the current date.
    
    Args:
        seed: Optional seed for reproducibility
    
    Returns:
        Tuple of (card, orientation)
    """
    if seed is None:
        # Use today's date as seed for consistent daily draw
        today = date.today()
        seed = hash(f"{today.year}-{today.month}-{today.day}")
    
    reader = TarotReader(seed=seed)
    return reader.draw_card(include_reversed=True)


def quick_reading(spread_type: str = "three_card", 
                 question: Optional[str] = None,
                 seed: Optional[int] = None) -> TarotReading:
    """
    Perform a quick reading.
    
    Args:
        spread_type: Type of spread ("one_card", "three_card", "celtic_cross", etc.)
        question: Optional question
        seed: Optional seed for reproducibility
    
    Returns:
        TarotReading object
    """
    reader = TarotReader(seed=seed)
    spread_map = {
        "one_card": reader.one_card_reading,
        "three_card": reader.three_card_reading,
        "celtic_cross": reader.celtic_cross_reading,
        "relationship": reader.relationship_reading,
        "decision": reader.decision_reading,
        "daily": reader.daily_reading,
        "horseshoe": reader.horseshoe_reading,
        "monthly": reader.monthly_reading
    }
    
    if spread_type not in spread_map:
        raise ValueError(f"Unknown spread type: {spread_type}. Available: {list(spread_map.keys())}")
    
    method = spread_map[spread_type]
    if spread_type in ["one_card", "three_card", "celtic_cross", "relationship", "decision", "horseshoe"]:
        return method(question=question)
    else:
        return method()


def get_major_arcana_cards() -> List[TarotCard]:
    """Get all Major Arcana cards."""
    deck = TarotDeck()
    return deck.get_major_arcana()


def get_minor_arcana_cards() -> List[TarotCard]:
    """Get all Minor Arcana cards."""
    deck = TarotDeck()
    return deck.get_minor_arcana()


def get_suit_cards(suit: str) -> List[TarotCard]:
    """
    Get all cards of a suit.
    
    Args:
        suit: Suit name ("wands", "cups", "swords", "pentacles")
    
    Returns:
        List of TarotCard objects
    """
    deck = TarotDeck()
    suit_enum = Suit(suit.lower())
    return deck.get_by_suit(suit_enum)


def search_cards_by_keyword(keyword: str) -> List[TarotCard]:
    """
    Search for cards by keyword.
    
    Args:
        keyword: Keyword to search for
    
    Returns:
        List of matching TarotCard objects
    """
    deck = TarotDeck()
    keyword = keyword.lower()
    return [c for c in deck.cards if any(keyword in k.lower() for k in c.keywords)]


def reading_for_date(target_date: date, spread_type: str = "three_card") -> TarotReading:
    """
    Get a reading for a specific date (reproducible).
    
    Args:
        target_date: Date for the reading
        spread_type: Type of spread
    
    Returns:
        TarotReading object
    """
    seed = hash(f"{target_date.year}-{target_date.month}-{target_date.day}")
    return quick_reading(spread_type, seed=seed)


def interpret_combination(cards: List[TarotCard]) -> str:
    """
    Provide a basic interpretation of card combinations.
    
    Args:
        cards: List of cards to interpret together
    
    Returns:
        Interpretation string
    """
    if not cards:
        return "No cards to interpret."
    
    # Count arcana types
    major_count = sum(1 for c in cards if c.arcana == Arcana.MAJOR)
    minor_count = len(cards) - major_count
    
    # Count elements
    elements = {}
    for card in cards:
        if card.element:
            elements[card.element] = elements.get(card.element, 0) + 1
    
    # Count suits
    suits = {}
    for card in cards:
        if card.suit:
            suits[card.suit.value] = suits.get(card.suit.value, 0) + 1
    
    interpretation = []
    
    # Major Arcana dominance
    if major_count > minor_count:
        interpretation.append("The reading is dominated by Major Arcana, indicating significant life events and karmic influences.")
    elif major_count == len(cards):
        interpretation.append("All Major Arcana cards - this is a powerful reading about major life themes.")
    
    # Element balance
    if elements:
        dominant_element = max(elements, key=elements.get)
        element_meanings = {
            "Fire": "strong energy, action, and passion",
            "Water": "emotions, intuition, and relationships",
            "Air": "mental activity, communication, and ideas",
            "Earth": "material matters, stability, and practicality"
        }
        if elements[dominant_element] >= len(cards) * 0.5:
            interpretation.append(f"Dominant {dominant_element} element suggests {element_meanings.get(dominant_element, 'significant influence')}.")
    
    # Suit balance
    if suits:
        dominant_suit = max(suits, key=suits.get)
        suit_meanings = {
            "wands": "creativity, career, and personal projects",
            "cups": "emotions, relationships, and spiritual matters",
            "swords": "intellect, communication, and challenges",
            "pentacles": "finances, material matters, and security"
        }
        if suits[dominant_suit] >= len(cards) * 0.5:
            interpretation.append(f"Dominant {dominant_suit} suit focuses on {suit_meanings.get(dominant_suit, 'key themes')}.")
    
    return " ".join(interpretation) if interpretation else "The cards present a balanced mix of influences."


# Export all
__all__ = [
    # Enums
    'Arcana',
    'Suit', 
    'Orientation',
    'SpreadType',
    # Classes
    'TarotCard',
    'TarotDeck',
    'SpreadPosition',
    'TarotReading',
    'TarotReader',
    # Data
    'MAJOR_ARCANA',
    'MINOR_ARCANA_COURT',
    'MINOR_ARCANA_NUMBERS',
    'SPREAD_DEFINITIONS',
    # Functions
    'get_card_by_name',
    'get_card_meaning',
    'daily_card',
    'quick_reading',
    'get_major_arcana_cards',
    'get_minor_arcana_cards',
    'get_suit_cards',
    'search_cards_by_keyword',
    'reading_for_date',
    'interpret_combination'
]