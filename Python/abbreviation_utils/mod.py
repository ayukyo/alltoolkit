"""
AllToolkit - Python Abbreviation & Acronym Utilities

A zero-dependency, production-ready abbreviation and acronym utility module.
Supports abbreviation expansion, detection, creation, and common abbreviation patterns.

Author: AllToolkit
License: MIT
"""

import re
from typing import Union, Optional, List, Dict, Tuple, Set
from dataclasses import dataclass


@dataclass
class AbbreviationInfo:
    """Abbreviation information container."""
    abbreviation: str
    expansion: str
    is_acronym: bool  # True if formed from first letters (e.g., NASA)
    is_initialism: bool  # True if pronounced letter-by-letter (e.g., FBI)
    category: str  # Organization, Technology, Medical, Common, etc.
    case_type: str  # uppercase, lowercase, mixed


# Common abbreviations and acronyms database
COMMON_ACRONYMS: Dict[str, Tuple[str, str]] = {
    # Organizations
    "NASA": ("National Aeronautics and Space Administration", "organization"),
    "FBI": ("Federal Bureau of Investigation", "organization"),
    "CIA": ("Central Intelligence Agency", "organization"),
    "UN": ("United Nations", "organization"),
    "EU": ("European Union", "organization"),
    "WHO": ("World Health Organization", "organization"),
    "UNICEF": ("United Nations Children's Fund", "organization"),
    "NATO": ("North Atlantic Treaty Organization", "organization"),
    "ASEAN": ("Association of Southeast Asian Nations", "organization"),
    "IMF": ("International Monetary Fund", "organization"),
    "WTO": ("World Trade Organization", "organization"),
    "UNESCO": ("United Nations Educational, Scientific and Cultural Organization", "organization"),
    "OPEC": ("Organization of the Petroleum Exporting Countries", "organization"),
    "FIFA": ("International Federation of Association Football", "organization"),
    "IOC": ("International Olympic Committee", "organization"),
    
    # Technology
    "API": ("Application Programming Interface", "technology"),
    "URL": ("Uniform Resource Locator", "technology"),
    "HTTP": ("Hypertext Transfer Protocol", "technology"),
    "HTTPS": ("Hypertext Transfer Protocol Secure", "technology"),
    "HTML": ("Hypertext Markup Language", "technology"),
    "CSS": ("Cascading Style Sheets", "technology"),
    "JavaScript": ("JavaScript", "technology"),  # Not an acronym
    "JSON": ("JavaScript Object Notation", "technology"),
    "XML": ("Extensible Markup Language", "technology"),
    "SQL": ("Structured Query Language", "technology"),
    "TCP": ("Transmission Control Protocol", "technology"),
    "IP": ("Internet Protocol", "technology"),
    "DNS": ("Domain Name System", "technology"),
    "FTP": ("File Transfer Protocol", "technology"),
    "SSH": ("Secure Shell", "technology"),
    "VPN": ("Virtual Private Network", "technology"),
    "LAN": ("Local Area Network", "technology"),
    "WAN": ("Wide Area Network", "technology"),
    "Wi-Fi": ("Wireless Fidelity", "technology"),
    "USB": ("Universal Serial Bus", "technology"),
    "CPU": ("Central Processing Unit", "technology"),
    "GPU": ("Graphics Processing Unit", "technology"),
    "RAM": ("Random Access Memory", "technology"),
    "ROM": ("Read-Only Memory", "technology"),
    "SSD": ("Solid State Drive", "technology"),
    "HDD": ("Hard Disk Drive", "technology"),
    "AI": ("Artificial Intelligence", "technology"),
    "ML": ("Machine Learning", "technology"),
    "NLP": ("Natural Language Processing", "technology"),
    "IoT": ("Internet of Things", "technology"),
    "VR": ("Virtual Reality", "technology"),
    "AR": ("Augmented Reality", "technology"),
    "SDK": ("Software Development Kit", "technology"),
    "IDE": ("Integrated Development Environment", "technology"),
    "GUI": ("Graphical User Interface", "technology"),
    "CLI": ("Command Line Interface", "technology"),
    "OS": ("Operating System", "technology"),
    "PDF": ("Portable Document Format", "technology"),
    "JPEG": ("Joint Photographic Experts Group", "technology"),
    "PNG": ("Portable Network Graphics", "technology"),
    "GIF": ("Graphics Interchange Format", "technology"),
    "SVG": ("Scalable Vector Graphics", "technology"),
    "MP3": ("MPEG Audio Layer III", "technology"),
    "MP4": ("MPEG-4 Part 14", "technology"),
    "MPEG": ("Moving Picture Experts Group", "technology"),
    "ISO": ("International Organization for Standardization", "technology"),
    
    # Business
    "CEO": ("Chief Executive Officer", "business"),
    "CFO": ("Chief Financial Officer", "business"),
    "CTO": ("Chief Technology Officer", "business"),
    "COO": ("Chief Operating Officer", "business"),
    "CIO": ("Chief Information Officer", "business"),
    "CMO": ("Chief Marketing Officer", "business"),
    "HR": ("Human Resources", "business"),
    "PR": ("Public Relations", "business"),
    "R&D": ("Research and Development", "business"),
    "ROI": ("Return on Investment", "business"),
    "KPI": ("Key Performance Indicator", "business"),
    "B2B": ("Business to Business", "business"),
    "B2C": ("Business to Consumer", "business"),
    "CRM": ("Customer Relationship Management", "business"),
    "ERP": ("Enterprise Resource Planning", "business"),
    "SaaS": ("Software as a Service", "business"),
    "PaaS": ("Platform as a Service", "business"),
    "IaaS": ("Infrastructure as a Service", "business"),
    "IPO": ("Initial Public Offering", "business"),
    "LLC": ("Limited Liability Company", "business"),
    "Inc": ("Incorporated", "business"),
    "Ltd": ("Limited", "business"),
    "Corp": ("Corporation", "business"),
    "FY": ("Fiscal Year", "business"),
    "Q1": ("First Quarter", "business"),
    "Q2": ("Second Quarter", "business"),
    "Q3": ("Third Quarter", "business"),
    "Q4": ("Fourth Quarter", "business"),
    "ETA": ("Estimated Time of Arrival", "business"),
    "TBA": ("To Be Announced", "business"),
    "TBD": ("To Be Determined", "business"),
    "ASAP": ("As Soon As Possible", "business"),
    
    # Medical
    "WHO": ("World Health Organization", "medical"),
    "CDC": ("Centers for Disease Control and Prevention", "medical"),
    "FDA": ("Food and Drug Administration", "medical"),
    "MRI": ("Magnetic Resonance Imaging", "medical"),
    "CT": ("Computed Tomography", "medical"),
    "X-ray": ("X-radiation", "medical"),
    "ICU": ("Intensive Care Unit", "medical"),
    "ER": ("Emergency Room", "medical"),
    "GP": ("General Practitioner", "medical"),
    "OB-GYN": ("Obstetrics and Gynecology", "medical"),
    "HIV": ("Human Immunodeficiency Virus", "medical"),
    "AIDS": ("Acquired Immunodeficiency Syndrome", "medical"),
    "CPR": ("Cardiopulmonary Resuscitation", "medical"),
    "DNA": ("Deoxyribonucleic Acid", "medical"),
    "RNA": ("Ribonucleic Acid", "medical"),
    "BMI": ("Body Mass Index", "medical"),
    "BP": ("Blood Pressure", "medical"),
    "OTC": ("Over the Counter", "medical"),
    
    # Academic/Education
    "PhD": ("Doctor of Philosophy", "academic"),
    "MBA": ("Master of Business Administration", "academic"),
    "BA": ("Bachelor of Arts", "academic"),
    "BS": ("Bachelor of Science", "academic"),
    "MA": ("Master of Arts", "academic"),
    "MS": ("Master of Science", "academic"),
    "MD": ("Doctor of Medicine", "academic"),
    "JD": ("Juris Doctor", "academic"),
    "LLB": ("Bachelor of Laws", "academic"),
    "LLM": ("Master of Laws", "academic"),
    "GPA": ("Grade Point Average", "academic"),
    "SAT": ("Scholastic Assessment Test", "academic"),
    "ACT": ("American College Testing", "academic"),
    "GRE": ("Graduate Record Examination", "academic"),
    "TOEFL": ("Test of English as a Foreign Language", "academic"),
    "IELTS": ("International English Language Testing System", "academic"),
    "STEM": ("Science, Technology, Engineering, and Mathematics", "academic"),
    
    # Government/Military
    "US": ("United States", "government"),
    "USA": ("United States of America", "government"),
    "DOD": ("Department of Defense", "government"),
    "DOE": ("Department of Energy", "government"),
    "EPA": ("Environmental Protection Agency", "government"),
    "FEMA": ("Federal Emergency Management Agency", "government"),
    "IRS": ("Internal Revenue Service", "government"),
    "SSN": ("Social Security Number", "government"),
    "DMV": ("Department of Motor Vehicles", "government"),
    "GPS": ("Global Positioning System", "government"),
    "USAF": ("United States Air Force", "government"),
    "USMC": ("United States Marine Corps", "government"),
    "USN": ("United States Navy", "government"),
    "USCG": ("United States Coast Guard", "government"),
    "NCO": ("Non-Commissioned Officer", "government"),
    
    # Common Abbreviations (not acronyms)
    "etc": ("et cetera", "common"),
    "e.g.": ("exempli gratia", "common"),
    "i.e.": ("id est", "common"),
    "vs": ("versus", "common"),
    "approx": ("approximately", "common"),
    "avg": ("average", "common"),
    "max": ("maximum", "common"),
    "min": ("minimum", "common"),
    "temp": ("temperature", "common"),
    "dept": ("department", "common"),
    "inst": ("institution", "common"),
    "rev": ("revision", "common"),
    "vol": ("volume", "common"),
    "no": ("number", "common"),
    "p": ("page", "common"),
    "pp": ("pages", "common"),
    "fig": ("figure", "common"),
    "ch": ("chapter", "common"),
    "sec": ("section", "common"),
    "ed": ("edition/editor", "common"),
    "vol": ("volume", "common"),
    "yr": ("year", "common"),
    "mo": ("month", "common"),
    "wk": ("week", "common"),
    "hr": ("hour", "common"),
    "min": ("minute", "common"),
    "sec": ("second", "common"),
    "ft": ("feet", "common"),
    "in": ("inch", "common"),
    "lb": ("pound", "common"),
    "oz": ("ounce", "common"),
    "kg": ("kilogram", "common"),
    "km": ("kilometer", "common"),
    "cm": ("centimeter", "common"),
    "mm": ("millimeter", "common"),
    "mg": ("milligram", "common"),
    "ml": ("milliliter", "common"),
    "mph": ("miles per hour", "common"),
    "kph": ("kilometers per hour", "common"),
    "rpm": ("revolutions per minute", "common"),
    "Hz": ("Hertz", "common"),
    "kHz": ("kilohertz", "common"),
    "MHz": ("megahertz", "common"),
    "GHz": ("gigahertz", "common"),
    "W": ("Watt", "common"),
    "kW": ("kilowatt", "common"),
    "MW": ("megawatt", "common"),
    "V": ("Volt", "common"),
    "A": ("Ampere", "common"),
    "kV": ("kilovolt", "common"),
    "mA": ("milliampere", "common"),
}

# State abbreviations (US)
US_STATES: Dict[str, str] = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}

# Country abbreviations
COUNTRY_CODES: Dict[str, str] = {
    "US": "United States", "UK": "United Kingdom", "CA": "Canada",
    "AU": "Australia", "NZ": "New Zealand", "DE": "Germany",
    "FR": "France", "IT": "Italy", "ES": "Spain", "PT": "Portugal",
    "NL": "Netherlands", "BE": "Belgium", "SE": "Sweden", "NO": "Norway",
    "DK": "Denmark", "FI": "Finland", "PL": "Poland", "GR": "Greece",
    "RU": "Russia", "CN": "China", "JP": "Japan", "KR": "South Korea",
    "IN": "India", "BR": "Brazil", "MX": "Mexico", "AR": "Argentina",
    "ZA": "South Africa", "EG": "Egypt", "NG": "Nigeria", "KE": "Kenya",
    "TH": "Thailand", "VN": "Vietnam", "MY": "Malaysia", "SG": "Singapore",
    "PH": "Philippines", "ID": "Indonesia", "TW": "Taiwan", "HK": "Hong Kong",
    "AE": "United Arab Emirates", "SA": "Saudi Arabia", "IL": "Israel",
    "TR": "Turkey", "IR": "Iran", "PK": "Pakistan", "BD": "Bangladesh",
    "UA": "Ukraine", "AT": "Austria", "CH": "Switzerland", "IE": "Ireland",
    "CZ": "Czech Republic", "RO": "Romania", "HU": "Hungary", "BG": "Bulgaria",
    "SK": "Slovakia", "SI": "Slovenia", "HR": "Croatia", "RS": "Serbia",
    "CL": "Chile", "CO": "Colombia", "PE": "Peru", "VE": "Venezuela",
    "CU": "Cuba", "JM": "Jamaica", "PR": "Puerto Rico",
}

# Regex patterns for abbreviation detection
# Pattern for common abbreviation formats
_ABBREVIATION_PATTERN = re.compile(
    r'\b([A-Z]{2,7})\b|'  # All uppercase words (2-7 letters)
    r'\b([A-Z][a-z]\.)\b|'  # Single letter followed by period (e.g., "Dr.")
    r'\b([A-Z]{2,4}\.[A-Z]{2,4})\b|'  # Multi-part abbreviations (e.g., "U.S.A.")
    r'\b([a-z]{2,4}\.)\b|'  # Lowercase with period (e.g., "etc.")
    r'\b([A-Z]/[A-Z]+)\b'  # Slash abbreviations (e.g., "R&D", "B2B")
)

# Pattern for detecting potential acronyms in text
_POTENTIAL_ACRONYM_PATTERN = re.compile(r'\b[A-Z]{2,}(?:s\b|\b)')


class AbbreviationUtils:
    """
    Abbreviation and acronym utility class.
    
    Provides functions for:
    - Expanding common abbreviations and acronyms
    - Detecting abbreviations in text
    - Creating abbreviations from words
    - Identifying acronym type (acronym vs initialism)
    - Handling state/country codes
    """
    
    # Build reverse lookup dictionary
    _EXPANSION_TO_ABBREV: Dict[str, str] = {}
    _reverse_lookup_built: bool = False
    
    @classmethod
    def _build_reverse_lookup(cls) -> None:
        """Build reverse lookup dictionary for expansion to abbreviation."""
        if not cls._reverse_lookup_built:
            cls._EXPANSION_TO_ABBREV = {}
            for abbrev, (expansion, _) in COMMON_ACRONYMS.items():
                cls._EXPANSION_TO_ABBREV[expansion.lower()] = abbrev
            cls._reverse_lookup_built = True
    
    def __init__(self):
        """Initialize abbreviation utilities."""
        self._build_reverse_lookup()
    
    @staticmethod
    def expand(abbreviation: str) -> Optional[str]:
        """
        Expand an abbreviation to its full form.
        
        Args:
            abbreviation: Abbreviation to expand (e.g., "NASA", "CEO")
        
        Returns:
            Full expansion, or None if not found
        
        Examples:
            >>> AbbreviationUtils.expand("NASA")
            'National Aeronautics and Space Administration'
            >>> AbbreviationUtils.expand("CEO")
            'Chief Executive Officer'
            >>> AbbreviationUtils.expand("unknown")
            None
        """
        # Check uppercase version first
        abbrev_upper = abbreviation.upper()
        abbrev_lower = abbreviation.lower()
        abbrev_original = abbreviation
        
        # Check in common acronyms
        if abbrev_upper in COMMON_ACRONYMS:
            return COMMON_ACRONYMS[abbrev_upper][0]
        
        if abbrev_original in COMMON_ACRONYMS:
            return COMMON_ACRONYMS[abbrev_original][0]
        
        # Check lowercase abbreviations (etc, e.g., i.e.)
        if abbrev_lower in COMMON_ACRONYMS:
            return COMMON_ACRONYMS[abbrev_lower][0]
        
        # Check US states
        if abbrev_upper in US_STATES:
            return US_STATES[abbrev_upper]
        
        # Check country codes
        if abbrev_upper in COUNTRY_CODES:
            return COUNTRY_CODES[abbrev_upper]
        
        return None
    
    @staticmethod
    def expand_text(text: str, keep_original: bool = False) -> str:
        """
        Expand all abbreviations in a text.
        
        Args:
            text: Text containing abbreviations
            keep_original: If True, keep abbreviation and add expansion
        
        Returns:
            Text with abbreviations expanded
        
        Examples:
            >>> AbbreviationUtils.expand_text("NASA launched a new rocket")
            'National Aeronautics and Space Administration launched a new rocket'
            >>> AbbreviationUtils.expand_text("NASA launched", keep_original=True)
            'National Aeronautics and Space Administration (NASA) launched'
        """
        if not text:
            return text
        
        result = text
        
        # Find all potential abbreviations
        matches = _ABBREVIATION_PATTERN.finditer(text)
        
        # Process matches in reverse order to maintain positions
        expansions = []
        for match in matches:
            for group_idx in range(1, 6):
                abbrev = match.group(group_idx)
                if abbrev:
                    expansion = AbbreviationUtils.expand(abbrev)
                    if expansion:
                        if keep_original:
                            replacement = f"{expansion} ({abbrev})"
                        else:
                            replacement = expansion
                        expansions.append((match.start(), match.end(), replacement, abbrev))
                    break
        
        # Apply expansions (reverse order to maintain correct positions)
        for start, end, replacement, abbrev in reversed(expansions):
            result = result[:start] + replacement + result[end:]
        
        return result
    
    @staticmethod
    def abbreviate(text: str, max_length: int = 4, style: str = "acronym") -> str:
        """
        Create an abbreviation from text.
        
        Args:
            text: Text to abbreviate
            max_length: Maximum length of abbreviation (default: 4)
            style: Abbreviation style - "acronym" (first letters), 
                   "truncation" (truncate words), or "hybrid"
        
        Returns:
            Abbreviated string
        
        Examples:
            >>> AbbreviationUtils.abbreviate("International Business Machines", style="acronym")
            'IBM'
            >>> AbbreviationUtils.abbreviate("Department of Motor Vehicles", style="acronym")
            'DMV'
            >>> AbbreviationUtils.abbreviate("Information Technology", style="acronym")
            'IT'
        """
        if not text:
            return ""
        
        words = text.split()
        
        if style == "acronym":
            # Take first letter of each significant word
            # Connector words to skip
            skip_words = {"of", "and", "the", "for", "in", "to", "a", "an", "by", "on", "at", "is", "or", "as"}
            acronym = ""
            for word in words:
                # Skip connector words regardless of length
                if word.lower() in skip_words:
                    continue
                # Take first letter, capitalize
                acronym += word[0].upper()
            
            # Limit to max_length
            return acronym[:max_length] if max_length else acronym
        
        elif style == "truncation":
            # Truncate each word to 4 characters max
            result = ""
            for word in words:
                if len(word) <= 4:
                    result += word + " "
                else:
                    result += word[:4] + ". "
            return result.strip()
        
        elif style == "hybrid":
            # First letter of important words, truncated for longer words
            result = ""
            for word in words:
                if len(word) <= 2 and word.lower() in {"of", "and", "the", "for", "in", "to", "a", "an"}:
                    continue
                if len(word) <= 4:
                    result += word[:2]
                else:
                    result += word[0].upper()
            return result[:max_length] if max_length else result
        
        return text
    
    @staticmethod
    def detect(text: str) -> List[AbbreviationInfo]:
        """
        Detect abbreviations in text.
        
        Args:
            text: Text to analyze
        
        Returns:
            List of AbbreviationInfo objects
        
        Examples:
            >>> abbrevs = AbbreviationUtils.detect("NASA and FBI work together")
            >>> len(abbrevs)
            2
            >>> abbrevs[0].abbreviation
            'NASA'
        """
        results = []
        
        matches = _ABBREVIATION_PATTERN.finditer(text)
        
        for match in matches:
            for group_idx in range(1, 6):
                abbrev = match.group(group_idx)
                if abbrev:
                    info = AbbreviationUtils.get_info(abbrev)
                    if info:
                        results.append(info)
                    break
        
        return results
    
    @staticmethod
    def get_info(abbreviation: str) -> Optional[AbbreviationInfo]:
        """
        Get detailed information about an abbreviation.
        
        Args:
            abbreviation: Abbreviation to analyze
        
        Returns:
            AbbreviationInfo object, or None if not recognized
        
        Examples:
            >>> info = AbbreviationUtils.get_info("NASA")
            >>> info.is_acronym
            True
            >>> info.category
            'organization'
        """
        abbrev_upper = abbreviation.upper()
        abbrev_lower = abbreviation.lower()
        abbrev_original = abbreviation
        
        # Check common acronyms
        if abbrev_upper in COMMON_ACRONYMS:
            expansion, category = COMMON_ACRONYMS[abbrev_upper]
            return AbbreviationInfo(
                abbreviation=abbrev_upper,
                expansion=expansion,
                is_acronym=AbbreviationUtils._is_acronym(abbrev_upper, expansion),
                is_initialism=AbbreviationUtils._is_initialism(abbrev_upper),
                category=category,
                case_type="uppercase"
            )
        
        if abbrev_original in COMMON_ACRONYMS:
            expansion, category = COMMON_ACRONYMS[abbrev_original]
            return AbbreviationInfo(
                abbreviation=abbrev_original,
                expansion=expansion,
                is_acronym=False,
                is_initialism=False,
                category=category,
                case_type="lowercase" if abbrev_original.islower() else "mixed"
            )
        
        if abbrev_lower in COMMON_ACRONYMS:
            expansion, category = COMMON_ACRONYMS[abbrev_lower]
            return AbbreviationInfo(
                abbreviation=abbrev_lower,
                expansion=expansion,
                is_acronym=False,
                is_initialism=False,
                category=category,
                case_type="lowercase"
            )
        
        # Check US states
        if abbrev_upper in US_STATES:
            return AbbreviationInfo(
                abbreviation=abbrev_upper,
                expansion=US_STATES[abbrev_upper],
                is_acronym=True,
                is_initialism=True,
                category="location",
                case_type="uppercase"
            )
        
        # Check country codes
        if abbrev_upper in COUNTRY_CODES:
            return AbbreviationInfo(
                abbreviation=abbrev_upper,
                expansion=COUNTRY_CODES[abbrev_upper],
                is_acronym=True,
                is_initialism=True,
                category="location",
                case_type="uppercase"
            )
        
        return None
    
    @staticmethod
    def _is_acronym(abbreviation: str, expansion: str) -> bool:
        """
        Check if abbreviation is an acronym (formed from first letters).
        
        Args:
            abbreviation: The abbreviation
            expansion: The full expansion
        
        Returns:
            True if formed from first letters of significant words
        """
        # Connector words to skip
        skip_words = {"of", "and", "the", "for", "in", "to", "a", "an", "by", "on", "at", "is", "or", "as"}
        
        # Get first letters of significant expansion words
        words = expansion.split()
        first_letters = "".join(w[0].upper() for w in words if w and w.lower() not in skip_words)
        
        return abbreviation.upper() == first_letters.upper()
    
    @staticmethod
    def _is_initialism(abbreviation: str) -> bool:
        """
        Check if abbreviation is an initialism (pronounced letter-by-letter).
        
        Initialisms are typically all uppercase and not pronounceable as words.
        
        Args:
            abbreviation: The abbreviation
        
        Returns:
            True if likely an initialism
        """
        if not abbreviation.isupper():
            return False
        
        # Known initialisms (pronounced letter-by-letter)
        # These contain vowels but are still initialisms
        known_initialisms = {
            "FBI", "CIA", "CIO", "CEO", "CFO", "CTO", "COO", "CMO",
            "URL", "SQL", "XML", "HTML", "HTTP", "HTTPS", "FTP", "DNS",
            "PDF", "USB", "CPU", "GPU", "LCD", "LED",
            "DNA", "RNA", "HIV", "GPA", "SAT", "ACT", "GRE",
            "USA", "UAE", "USMC", "USAF", "USCG", "USN",
            "IRS", "DOD", "DOE", "EPA", "FEMA", "SSN", "DMV", "NCO",
        }
        
        # Known acronyms (pronounced as words)
        known_acronyms = {
            "NASA", "NATO", "UNESCO", "UNICEF", "OPEC", "ASEAN",
            "RAM", "ROM", "RAID", "SATA", "SCSI",
            "JPEG", "MPEG", "WAV", "LASER", "RADAR",
            "SIM", "PIN", "VIN", "SWAT", "OSHA",
            "NIMH", "AARP", "PETA", "UN",
        }
        
        # Check known lists first
        if abbreviation in known_initialisms:
            return True
        if abbreviation in known_acronyms:
            return False
        
        # Heuristic for unknown abbreviations
        # If it's 2 letters, it's almost always an initialism
        if len(abbreviation) <= 2:
            return True
        
        # Check for pronounceability patterns
        # Acronyms typically have vowels in syllable-friendly positions
        vowels = set("AEIOU")
        has_vowels = any(c in vowels for c in abbreviation)
        
        if not has_vowels:
            # No vowels = definitely an initialism
            return True
        
        # Has vowels - use letter position heuristic
        # If abbreviation starts with vowel, it's more likely an acronym
        # (e.g., ASEAN, UNESCO start with vowels and are pronounceable)
        if abbreviation[0] in vowels:
            return False
        
        # If there's a good vowel/consonant pattern for pronouncing
        # e.g., NATO (N-A-T-O) has alternating pattern
        vowel_positions = [i for i, c in enumerate(abbreviation) if c in vowels]
        
        # If vowels are well-spaced (syllable pattern), it's likely an acronym
        if len(vowel_positions) >= 2:
            avg_spacing = sum(vowel_positions[i+1] - vowel_positions[i] 
                             for i in range(len(vowel_positions)-1)) / (len(vowel_positions)-1)
            if avg_spacing <= 2:  # Good syllable pattern
                return False
        
        # Default: shorter or less pronounceable patterns = initialism
        return len(abbreviation) <= 4
    
    @staticmethod
    def is_abbreviation(text: str) -> bool:
        """
        Check if text is a known abbreviation.
        
        Args:
            text: Text to check
        
        Returns:
            True if recognized as abbreviation
        
        Examples:
            >>> AbbreviationUtils.is_abbreviation("NASA")
            True
            >>> AbbreviationUtils.is_abbreviation("Hello")
            False
        """
        return AbbreviationUtils.expand(text) is not None
    
    @staticmethod
    def find_abbreviation_for(expansion: str) -> Optional[str]:
        """
        Find abbreviation for a given expansion.
        
        Args:
            expansion: Full text to abbreviate
        
        Returns:
            Known abbreviation, or None
        
        Examples:
            >>> AbbreviationUtils.find_abbreviation_for("National Aeronautics and Space Administration")
            'NASA'
        """
        # Build reverse lookup if not exists
        if not AbbreviationUtils._EXPANSION_TO_ABBREV:
            AbbreviationUtils._build_reverse_lookup()
        
        expansion_lower = expansion.lower()
        
        # Check direct match
        if expansion_lower in AbbreviationUtils._EXPANSION_TO_ABBREV:
            return AbbreviationUtils._EXPANSION_TO_ABBREV[expansion_lower]
        
        # Try to abbreviate and check if it exists
        created_abbrev = AbbreviationUtils.abbreviate(expansion, style="acronym")
        if created_abbrev in COMMON_ACRONYMS:
            return created_abbrev
        
        return None
    
    @staticmethod
    def get_all_by_category(category: str) -> Dict[str, str]:
        """
        Get all abbreviations in a specific category.
        
        Args:
            category: Category name (organization, technology, business, etc.)
        
        Returns:
            Dictionary of abbreviations and expansions
        
        Examples:
            >>> tech_abbrevs = AbbreviationUtils.get_all_by_category("technology")
            >>> 'API' in tech_abbrevs
            True
        """
        result = {}
        for abbrev, (expansion, cat) in COMMON_ACRONYMS.items():
            if cat == category:
                result[abbrev] = expansion
        return result
    
    @staticmethod
    def get_categories() -> List[str]:
        """
        Get all available categories.
        
        Returns:
            List of category names
        
        Examples:
            >>> categories = AbbreviationUtils.get_categories()
            >>> 'technology' in categories
            True
        """
        categories = set()
        for _, (_, cat) in COMMON_ACRONYMS.items():
            categories.add(cat)
        return sorted(list(categories))
    
    @staticmethod
    def add_custom(abbreviation: str, expansion: str, category: str = "custom") -> None:
        """
        Add a custom abbreviation.
        
        Args:
            abbreviation: Abbreviation to add
            expansion: Full expansion
            category: Category name
        
        Examples:
            >>> AbbreviationUtils.add_custom("MYCO", "My Custom Organization")
            >>> AbbreviationUtils.expand("MYCO")
            'My Custom Organization'
        """
        COMMON_ACRONYMS[abbreviation] = (expansion, category)
        AbbreviationUtils._EXPANSION_TO_ABBREV[expansion.lower()] = abbreviation
    
    @staticmethod
    def expand_state(state_code: str) -> Optional[str]:
        """
        Expand US state abbreviation.
        
        Args:
            state_code: Two-letter state code
        
        Returns:
            State name, or None
        
        Examples:
            >>> AbbreviationUtils.expand_state("CA")
            'California'
            >>> AbbreviationUtils.expand_state("NY")
            'New York'
        """
        return US_STATES.get(state_code.upper())
    
    @staticmethod
    def abbreviate_state(state_name: str) -> Optional[str]:
        """
        Get abbreviation for US state name.
        
        Args:
            state_name: Full state name
        
        Returns:
            Two-letter code, or None
        
        Examples:
            >>> AbbreviationUtils.abbreviate_state("California")
            'CA'
        """
        for code, name in US_STATES.items():
            if name.lower() == state_name.lower():
                return code
        return None
    
    @staticmethod
    def expand_country(country_code: str) -> Optional[str]:
        """
        Expand country code abbreviation.
        
        Args:
            country_code: Two-letter country code
        
        Returns:
            Country name, or None
        
        Examples:
            >>> AbbreviationUtils.expand_country("US")
            'United States'
            >>> AbbreviationUtils.expand_country("CN")
            'China'
        """
        return COUNTRY_CODES.get(country_code.upper())
    
    @staticmethod
    def abbreviate_country(country_name: str) -> Optional[str]:
        """
        Get abbreviation for country name.
        
        Args:
            country_name: Full country name
        
        Returns:
            Two-letter code, or None
        
        Examples:
            >>> AbbreviationUtils.abbreviate_country("United States")
            'US'
        """
        for code, name in COUNTRY_CODES.items():
            if name.lower() == country_name.lower():
                return code
        return None
    
    @staticmethod
    def count_abbreviations(text: str) -> Dict[str, int]:
        """
        Count occurrences of abbreviations in text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with abbreviation counts
        
        Examples:
            >>> counts = AbbreviationUtils.count_abbreviations("NASA and NASA work with FBI")
            >>> counts['NASA']
            2
        """
        counts = {}
        matches = _ABBREVIATION_PATTERN.finditer(text)
        
        for match in matches:
            for group_idx in range(1, 6):
                abbrev = match.group(group_idx)
                if abbrev and AbbreviationUtils.is_abbreviation(abbrev):
                    counts[abbrev] = counts.get(abbrev, 0) + 1
                    break
        
        return counts


# Convenience functions for direct import

def expand(abbreviation: str) -> Optional[str]:
    """Expand an abbreviation to its full form."""
    return AbbreviationUtils.expand(abbreviation)


def expand_text(text: str, keep_original: bool = False) -> str:
    """Expand all abbreviations in text."""
    return AbbreviationUtils.expand_text(text, keep_original)


def abbreviate(text: str, max_length: int = 4, style: str = "acronym") -> str:
    """Create an abbreviation from text."""
    return AbbreviationUtils.abbreviate(text, max_length, style)


def detect(text: str) -> List[AbbreviationInfo]:
    """Detect abbreviations in text."""
    return AbbreviationUtils.detect(text)


def get_info(abbreviation: str) -> Optional[AbbreviationInfo]:
    """Get detailed information about an abbreviation."""
    return AbbreviationUtils.get_info(abbreviation)


def is_abbreviation(text: str) -> bool:
    """Check if text is a known abbreviation."""
    return AbbreviationUtils.is_abbreviation(text)


def find_abbreviation_for(expansion: str) -> Optional[str]:
    """Find abbreviation for a given expansion."""
    return AbbreviationUtils.find_abbreviation_for(expansion)


def expand_state(state_code: str) -> Optional[str]:
    """Expand US state abbreviation."""
    return AbbreviationUtils.expand_state(state_code)


def abbreviate_state(state_name: str) -> Optional[str]:
    """Get abbreviation for US state name."""
    return AbbreviationUtils.abbreviate_state(state_name)


def expand_country(country_code: str) -> Optional[str]:
    """Expand country code abbreviation."""
    return AbbreviationUtils.expand_country(country_code)


def abbreviate_country(country_name: str) -> Optional[str]:
    """Get abbreviation for country name."""
    return AbbreviationUtils.abbreviate_country(country_name)


def get_all_by_category(category: str) -> Dict[str, str]:
    """Get all abbreviations in a specific category."""
    return AbbreviationUtils.get_all_by_category(category)


def get_categories() -> List[str]:
    """Get all available categories."""
    return AbbreviationUtils.get_categories()


def add_custom(abbreviation: str, expansion: str, category: str = "custom") -> None:
    """Add a custom abbreviation."""
    return AbbreviationUtils.add_custom(abbreviation, expansion, category)


def count_abbreviations(text: str) -> Dict[str, int]:
    """Count occurrences of abbreviations in text."""
    return AbbreviationUtils.count_abbreviations(text)


if __name__ == '__main__':
    # Demo
    print("=== Abbreviation Utilities Demo ===")
    
    # Expand abbreviations
    print("\n--- Expand Examples ---")
    print(f"NASA -> {expand('NASA')}")
    print(f"CEO -> {expand('CEO')}")
    print(f"API -> {expand('API')}")
    print(f"CA (state) -> {expand('CA')}")
    print(f"US (country) -> {expand('US')}")
    
    # Expand text
    print("\n--- Expand Text Examples ---")
    text = "NASA and FBI collaborated with the CIA on the project."
    print(f"Original: {text}")
    print(f"Expanded: {expand_text(text)}")
    print(f"With original: {expand_text(text, keep_original=True)}")
    
    # Create abbreviations
    print("\n--- Create Abbreviations ---")
    print(f"International Business Machines -> {abbreviate('International Business Machines')}")
    print(f"Department of Motor Vehicles -> {abbreviate('Department of Motor Vehicles')}")
    
    # Detect abbreviations
    print("\n--- Detect Abbreviations ---")
    text = "The CEO and CFO met with the FBI and NASA representatives."
    detected = detect(text)
    for info in detected:
        print(f"{info.abbreviation}: {info.expansion} ({info.category})")
    
    # Get categories
    print("\n--- Categories ---")
    print(f"Available: {get_categories()}")
    
    # State and country
    print("\n--- Location Abbreviations ---")
    print(f"California -> {abbreviate_state('California')}")
    print(f"CA -> {expand_state('CA')}")
    print(f"United States -> {abbreviate_country('United States')}")
    print(f"US -> {expand_country('US')}")