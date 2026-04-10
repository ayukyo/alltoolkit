"""
AllToolkit - Python Email Utilities

A zero-dependency, production-ready email utility module.
Supports email validation, parsing, formatting, normalization, and domain analysis.

Author: AllToolkit
License: MIT
"""

import re
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass


@dataclass
class EmailAddress:
    """Represents a parsed email address."""
    local: str          # Local part (before @)
    domain: str         # Domain part (after @)
    original: str       # Original email string
    normalized: str     # Normalized email (lowercase domain)
    is_valid: bool      # Validation result
    display_name: Optional[str] = None  # Optional display name


class EmailUtils:
    """
    Email address utilities.
    
    Provides functions for:
    - Email validation (RFC 5322 compliant)
    - Email parsing and normalization
    - Domain analysis (MX record hints, disposable detection)
    - Email formatting and obfuscation
    - Bulk email processing
    """

    # RFC 5322 compliant email regex (simplified but practical)
    # Local part: allows letters, digits, and special chars ._%+-
    # Domain part: allows letters, digits, hyphens, and dots
    EMAIL_REGEX = re.compile(
        r'^(?P<local>[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+)'
        r'@'
        r'(?P<domain>[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
        r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)$'
    )

    # Display name with email pattern: "Name" <email@example.com>
    DISPLAY_EMAIL_REGEX = re.compile(
        r'^(?:"?(?P<name>[^"<]*)"?|(?P<name2>[^<]*))\s*'
        r'<(?P<email>[^>]+)>$'
    )

    # Known disposable email domains (partial list)
    DISPOSABLE_DOMAINS = frozenset([
        '10minutemail.com', 'tempmail.com', 'guerrillamail.com',
        'mailinator.com', 'throwaway.email', 'temp-mail.org',
        'fakeinbox.com', 'trashmail.com', 'yopmail.com',
        'getnada.com', 'maildrop.cc', 'sharklasers.com',
        'grr.la', 'guerrillamailblock.com', 'pokemail.net',
        'spam4.me', 'bccto.me', 'chacuo.net', 'dispostable.com',
        'emkei.cz', 'emailondeck.com', 'getairmail.com',
        'hidemail.de', 'mytrashmail.com', 'no-spam.ws',
        'nowmymail.com', 'put2.net', 'quickinbox.com',
        'rcpt.at', 'safe-mail.net', 'selfdestructingmail.com',
        'sendspamhere.com', 'tempemail.com', 'tempinbox.com',
        'thankyou2010.com', 'thisisnotmyrealemail.com',
        'throwam.com', 'tilien.com', 'tradermail.info',
        'trash-email.com', 'trashmail.at', 'trashmail.de',
        'trashmail.me', 'trashmail.net', 'trashmail.org',
        'wegwerfmail.de', 'wegwerfmail.net', 'wegwerfmail.org',
        'wh4f.org', 'whyspam.me', 'willselfdestruct.com',
        'xoxy.net', 'yogamail.com', 'zehnminutenmail.de',
        'jetable.com', 'jetable.fr.nf', 'jetable.net',
        'jetable.org', 'gishpuppy.com', 'mailcatch.com',
        'mailexpire.com', 'mailforspam.com', 'mailfreeonline.com',
        'mailguard.me', 'mailnesia.com', 'mailtemp.info',
        'mintemail.com', 'mohmal.com', 'mohmal.im',
        'mohmal.in', 'mohmal.tech', 'mytemp.email',
        'nospam4me.com', 'nospamfor.us', 'nospamthanks.com',
        'notmailinator.com', 'nowhere.org', 'objectmail.com',
        'obobbo.com', 'oneoffemail.com', 'oneoffmail.com',
        'ordinaryamerican.net', 'otherinbox.com', 'ourklips.com',
        'outlawspam.com', 'pancakemail.com', 'pjjkp.com',
        'plexolan.de', 'poczta.onet.pl', 'politikerclub.de',
        'pookmail.com', 'privacy.net', 'proxymail.eu',
        'prtnx.com', 'punkass.com', 'purespam.com',
        'qisdo.com', 'qisoa.com', 'quickemailverification.com',
        'raakim.com', 'rhyta.com', 'rmqkr.net',
        'royal.net', 'rppkn.com', 'rtrtr.com',
        's0ny.net', 'safe-gmbh.net', 'safe-mail.net',
        'safersignup.de', 'safetymail.info', 'safetypost.de',
        'sandelf.de', 'saynotospams.com', 'schafmail.de',
        'secretemail.de', 'sharklasers.com', 'shieldedmail.com',
        'shortmail.net', 'sibmail.com', 'sinnlos-mail.de',
        'slapsfromlastnight.com', 'slaskpost.se', 'smashmail.de',
        'smellfear.com', 'sneakemail.com', 'sneakmail.de',
        'sofimail.com', 'sofort-mail.de', 'sofortmail.de',
        'sogetmail.com', 'spam.la', 'spam.su',
        'spam4.me', 'spamavert.com', 'spambob.com',
        'spambob.net', 'spambob.org', 'spambog.com',
        'spambog.de', 'spambog.net', 'spambog.ru',
        'spambox.info', 'spambox.irishspringrealty.com',
        'spambox.us', 'spamcannon.com', 'spamcannon.net',
        'spamcero.com', 'spamcon.org', 'spamcorptastic.com',
        'spamcowboy.com', 'spamcowboy.net', 'spamcowboy.org',
        'spamday.com', 'spamdecoy.net', 'spamex.com',
        'spamfree24.com', 'spamfree24.de', 'spamfree24.eu',
        'spamfree24.info', 'spamfree24.net', 'spamfree24.org',
        'spamgoes.in', 'spamgourmet.com', 'spamgourmet.net',
        'spamgourmet.org', 'spamherelots.com', 'spamhereplease.com',
        'spamhole.com', 'spamify.com', 'spaminator.de',
        'spamkill.info', 'spaml.com', 'spaml.de',
        'spammotel.com', 'spamobox.com', 'spamoff.de',
        'spamslicer.com', 'spamspot.com', 'spamstack.net',
        'spamthis.co.uk', 'spamthisplease.com', 'spamtrail.com',
        'spamtroll.net', 'speed.1s.fr', 'spoofmail.de',
        'stuffmail.de', 'super-auswahl.de', 'supergreatmail.com',
        'supermailer.jp', 'superrito.com', 'superstachel.de',
        'suremail.info', 'talkinator.com', 'temp-mail.com',
        'temp-mail.de', 'temp-mail.org', 'temp-mail.ru',
        'temp.headstrong.de', 'tempemail.co.za', 'tempemail.com',
        'tempemail.net', 'tempinbox.co.uk', 'tempinbox.com',
        'tempmail.co', 'tempmail.de', 'tempmaildemo.com',
        'tempmailer.com', 'tempmailer.de', 'tempomail.fr',
        'temporarily.de', 'temporarioemail.com.br', 'temporaryemail.net',
        'temporaryforwarding.com', 'temporaryinbox.com', 'temporarymailaddress.com',
        'tempthe.net', 'tempymail.com', 'thanksnospam.info',
        'thankyou2010.com', 'thecloudindex.com', 'thisisnotmyrealemail.com',
        'thismail.net', 'throwawayemailaddress.com', 'throwawaymail.com',
        'tilien.com', 'tittbit.in', 'tizi.com',
        'tmail.ws', 'tmailinator.com', 'toiea.com',
        'toomail.biz', 'topranklist.de', 'tradermail.info',
        'trash-amil.com', 'trash-mail.at', 'trash-mail.com',
        'trash-mail.de', 'trash-mail.ml', 'trash2009.com',
        'trash2010.com', 'trash2011.com', 'trashdevil.com',
        'trashdevil.de', 'trashemail.de', 'trashmail.at',
        'trashmail.com', 'trashmail.de', 'trashmail.me',
        'trashmail.net', 'trashmail.org', 'trashymail.com',
        'trayna.com', 'trbvm.com', 'trbvn.com',
        'trollproject.com', 'tropicalbass.info', 'trungtamnhantam.com',
        'tryalert.com', 'turual.com', 'twinmail.de',
        'tyldd.com', 'uggsrock.com', 'umail.net',
        'upliftnow.com', 'uplipht.com', 'uroid.com',
        'us.af', 'venompen.com', 'veryrealemail.com',
        'viditag.com', 'viewcastmedia.com', 'viewcastmedia.net',
        'viewcastmedia.org', 'viralplays.com', 'vomoto.com',
        'vubby.com', 'wasteland.rfc822.org', 'webemail.me',
        'webm4il.info', 'wegwerfadresse.de', 'wegwerfemail.de',
        'wegwerfmail.de', 'wegwerfmail.info', 'wegwerfmail.net',
        'wegwerfmail.org', 'wh4f.org', 'whatiaas.com',
        'whatpaas.com', 'whatsaas.com', 'whopy.com',
        'whyspam.me', 'wmail.cf', 'writeme.us',
        'wronghead.com', 'wuzupmail.net', 'xoxy.net',
        'yogamail.com', 'yopmail.com', 'yopmail.fr',
        'yopmail.net', 'yopmail.org', 'youmailr.com',
        'yourdomain.com', 'z1p.biz', 'zehnminutenmail.de',
        'zetmail.com', 'zippymail.info', 'zoaxe.com',
        'zoemail.com', 'zoemail.net', 'zoemail.org',
        'zomg.info', 'zxcv.com', 'zxcvbnm.com',
        'zybermail.com', 'zybermail.de', 'zehnminuten.de'
    ])

    # Common free email providers
    FREE_PROVIDERS = frozenset([
        'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.uk',
        'yahoo.co.jp', 'yahoo.de', 'yahoo.fr', 'yahoo.it',
        'yahoo.es', 'hotmail.com', 'hotmail.co.uk', 'hotmail.de',
        'hotmail.fr', 'outlook.com', 'outlook.co.uk', 'outlook.de',
        'outlook.fr', 'live.com', 'live.co.uk', 'live.de',
        'live.fr', 'msn.com', 'aol.com', 'aol.co.uk',
        'icloud.com', 'me.com', 'mac.com', 'mail.com',
        'protonmail.com', 'proton.me', 'tutanota.com', 'tuta.io',
        'gmx.com', 'gmx.de', 'gmx.net', 'web.de',
        'yandex.com', 'yandex.ru', 'mail.ru', 'bk.ru',
        'inbox.ru', 'list.ru', 'qq.com', '163.com',
        '126.com', 'sina.com', 'sohu.com', 'foxmail.com',
        'aliyun.com', 'tom.com', '21cn.com', 'yeah.net'
    ])

    # Pre-compiled regex patterns for performance
    _CONSECUTIVE_DOTS = re.compile(r'\.\.')
    _TLD_ALPHA = re.compile(r'^[a-zA-Z]+$')
    
    @staticmethod
    def validate(email: str) -> bool:
        """
        Validate an email address.
        
        Checks:
        - Basic format (local@domain)
        - Local part length (max 64 chars)
        - Domain length (max 255 chars)
        - Domain has valid TLD (2+ chars)
        - No consecutive dots
        - No leading/trailing dots in local part

        Args:
            email: Email address to validate

        Returns:
            True if valid, False otherwise

        Example:
            >>> EmailUtils.validate("user@example.com")
            True
            >>> EmailUtils.validate("invalid@")
            False
        """
        if not email or not isinstance(email, str):
            return False
        
        email = email.strip()
        
        # Quick length check (RFC 5321 max: 64@255 = 320)
        email_len = len(email)
        if email_len > 320 or email_len < 3:  # minimum: a@b
            return False
        
        # Fast path: check for @ symbol
        at_idx = email.find('@')
        if at_idx <= 0 or at_idx == email_len - 1:
            return False
        
        # Basic regex match
        match = EmailUtils.EMAIL_REGEX.match(email)
        if not match:
            return False
        
        local = match.group('local')
        domain = match.group('domain')
        
        # Local part checks
        if len(local) > 64 or local.startswith('.') or local.endswith('.'):
            return False
        if EmailUtils._CONSECUTIVE_DOTS.search(local):
            return False
        
        # Domain checks
        if len(domain) > 255 or domain.startswith('.') or domain.endswith('.'):
            return False
        if EmailUtils._CONSECUTIVE_DOTS.search(domain):
            return False
        
        # TLD validation: must have at least one dot and valid TLD
        dot_idx = domain.rfind('.')
        if dot_idx <= 0 or dot_idx == len(domain) - 1:
            return False
        
        tld = domain[dot_idx + 1:]
        if len(tld) < 2 or not EmailUtils._TLD_ALPHA.match(tld):
            return False
        
        return True

    @staticmethod
    def parse(email: str) -> Optional[EmailAddress]:
        """
        Parse an email address into components.
        
        Handles formats:
        - Simple: user@example.com
        - With display name: "John Doe" <user@example.com>
        - With display name: John Doe <user@example.com>

        Args:
            email: Email address string (may include display name)

        Returns:
            EmailAddress object or None if invalid

        Example:
            >>> result = EmailUtils.parse("user@example.com")
            >>> result.local
            'user'
            >>> result.domain
            'example.com'
        """
        if not email or not isinstance(email, str):
            return None
        
        email = email.strip()
        display_name = None
        
        # Check for display name format
        display_match = EmailUtils.DISPLAY_EMAIL_REGEX.match(email)
        if display_match:
            display_name = display_match.group('name') or display_match.group('name2')
            email = display_match.group('email').strip()
            display_name = display_name.strip() if display_name else None
        
        # Validate the email part
        if not EmailUtils.validate(email):
            return None
        
        # Parse local and domain
        match = EmailUtils.EMAIL_REGEX.match(email)
        if not match:
            return None
        
        local = match.group('local')
        domain = match.group('domain')
        
        # Normalized: lowercase domain
        normalized = f"{local}@{domain.lower()}"
        
        return EmailAddress(
            local=local,
            domain=domain,
            original=email,
            normalized=normalized,
            is_valid=True,
            display_name=display_name
        )

    @staticmethod
    def normalize(email: str) -> Optional[str]:
        """
        Normalize an email address.
        
        Normalization:
        - Lowercase domain
        - Lowercase local part
        - Remove dots from Gmail local part (Gmail ignores dots)
        - Remove everything after + in local part (subaddressing)

        Args:
            email: Email address to normalize

        Returns:
            Normalized email or None if invalid

        Example:
            >>> EmailUtils.normalize("User+tag@Gmail.com")
            'user@gmail.com'
            >>> EmailUtils.normalize("first.last@gmail.com")
            'firstlast@gmail.com'
        """
        parsed = EmailUtils.parse(email)
        if not parsed:
            return None
        
        local = parsed.local.lower()
        domain = parsed.domain.lower()
        
        # Gmail-specific normalization
        if domain in ('gmail.com', 'googlemail.com'):
            # Remove everything after +
            if '+' in local:
                local = local.split('+')[0]
            # Remove dots
            local = local.replace('.', '')
        
        # Generic subaddressing removal (after +)
        elif '+' in local:
            local = local.split('+')[0]
        
        return f"{local}@{domain}"

    @staticmethod
    def is_disposable(email: str) -> bool:
        """
        Check if email is from a disposable/temporary email provider.

        Args:
            email: Email address to check

        Returns:
            True if disposable, False otherwise

        Example:
            >>> EmailUtils.is_disposable("user@mailinator.com")
            True
            >>> EmailUtils.is_disposable("user@gmail.com")
            False
        """
        parsed = EmailUtils.parse(email)
        if not parsed:
            return False
        
        domain = parsed.domain.lower()
        return domain in EmailUtils.DISPOSABLE_DOMAINS

    @staticmethod
    def is_free_provider(email: str) -> bool:
        """
        Check if email is from a common free email provider.

        Args:
            email: Email address to check

        Returns:
            True if from free provider, False otherwise

        Example:
            >>> EmailUtils.is_free_provider("user@gmail.com")
            True
            >>> EmailUtils.is_free_provider("user@company.com")
            False
        """
        parsed = EmailUtils.parse(email)
        if not parsed:
            return False
        
        domain = parsed.domain.lower()
        return domain in EmailUtils.FREE_PROVIDERS

    @staticmethod
    def get_domain(email: str) -> Optional[str]:
        """
        Extract the domain from an email address.

        Args:
            email: Email address

        Returns:
            Domain string or None if invalid

        Example:
            >>> EmailUtils.get_domain("user@example.com")
            'example.com'
        """
        parsed = EmailUtils.parse(email)
        return parsed.domain if parsed else None

    @staticmethod
    def get_local(email: str) -> Optional[str]:
        """
        Extract the local part from an email address.

        Args:
            email: Email address

        Returns:
            Local part string or None if invalid

        Example:
            >>> EmailUtils.get_local("user@example.com")
            'user'
        """
        parsed = EmailUtils.parse(email)
        return parsed.local if parsed else None

    @staticmethod
    def obfuscate(email: str, show_chars: int = 2) -> Optional[str]:
        """
        Obfuscate an email address for display.
        
        Shows first N characters of local part, replaces rest with asterisks.
        Uses fixed 7 asterisks for consistent obfuscation appearance.

        Args:
            email: Email address to obfuscate
            show_chars: Number of characters to show (default: 2)

        Returns:
            Obfuscated email or None if invalid

        Example:
            >>> EmailUtils.obfuscate("john.doe@example.com")
            'jo*******@example.com'
        """
        # Validate show_chars
        if not isinstance(show_chars, int) or show_chars < 0:
            show_chars = 2
        
        parsed = EmailUtils.parse(email)
        if not parsed:
            return None
        
        local = parsed.local
        domain = parsed.domain
        
        # Handle edge cases
        if not local:
            return f"*******@{domain}"
        
        if len(local) <= show_chars:
            obfuscated_local = local
        else:
            visible = local[:show_chars]
            # Use fixed 7 asterisks for consistent obfuscation appearance
            obfuscated_local = visible + '*' * 7
        
        return f"{obfuscated_local}@{domain}"

    @staticmethod
    def format_with_name(email: str, name: Optional[str] = None) -> Optional[str]:
        """
        Format email with display name.

        Args:
            email: Email address
            name: Display name (optional, can be extracted from parsed email)

        Returns:
            Formatted string like "Name" <email@example.com>

        Example:
            >>> EmailUtils.format_with_name("user@example.com", "John Doe")
            '"John Doe" <user@example.com>'
        """
        parsed = EmailUtils.parse(email)
        if not parsed:
            return None
        
        if name is None:
            name = parsed.display_name
        
        if name:
            # Quote name if it contains spaces or special chars
            if ' ' in name or '"' in name or '<' in name:
                # Escape quotes in name
                escaped_name = name.replace('"', '\\"')
                return f'"{escaped_name}" <{parsed.normalized}>'
            else:
                return f'{name} <{parsed.normalized}>'
        
        return parsed.normalized

    @staticmethod
    def extract_from_text(text: str) -> List[str]:
        """
        Extract all email addresses from text.

        Args:
            text: Text to search for emails

        Returns:
            List of found email addresses

        Example:
            >>> EmailUtils.extract_from_text("Contact us at support@example.com")
            ['support@example.com']
        """
        if not text or not isinstance(text, str):
            return []
        
        # Find all potential email patterns
        pattern = r'[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*'
        
        candidates = re.findall(pattern, text)
        
        # Validate each candidate
        valid_emails = []
        for candidate in candidates:
            if EmailUtils.validate(candidate):
                valid_emails.append(candidate)
        
        return valid_emails

    @staticmethod
    def deduplicate(emails: List[str]) -> List[str]:
        """
        Remove duplicate emails (case-insensitive, normalized).

        Args:
            emails: List of email addresses

        Returns:
            Deduplicated list preserving original order

        Example:
            >>> EmailUtils.deduplicate(["User@Example.com", "user@example.com"])
            ['User@Example.com']
        """
        seen = set()
        result = []
        
        for email in emails:
            normalized = EmailUtils.normalize(email)
            if normalized and normalized.lower() not in seen:
                seen.add(normalized.lower())
                result.append(email)
        
        return result

    @staticmethod
    def sort_by_domain(emails: List[str]) -> List[str]:
        """
        Sort emails by domain, then by local part.

        Args:
            emails: List of email addresses

        Returns:
            Sorted list

        Example:
            >>> emails = ["b@yahoo.com", "a@gmail.com", "c@gmail.com"]
            >>> EmailUtils.sort_by_domain(emails)
            ['a@gmail.com', 'c@gmail.com', 'b@yahoo.com']
        """
        def sort_key(email: str) -> Tuple[str, str]:
            parsed = EmailUtils.parse(email)
            if parsed:
                return (parsed.domain.lower(), parsed.local.lower())
            return ('', email.lower())
        
        return sorted(emails, key=sort_key)

    @staticmethod
    def group_by_domain(emails: List[str]) -> Dict[str, List[str]]:
        """
        Group emails by their domain.

        Args:
            emails: List of email addresses

        Returns:
            Dictionary mapping domains to lists of emails

        Example:
            >>> emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com"]
            >>> result = EmailUtils.group_by_domain(emails)
            >>> result['gmail.com']
            ['a@gmail.com', 'c@gmail.com']
        """
        groups: Dict[str, List[str]] = {}
        
        for email in emails:
            parsed = EmailUtils.parse(email)
            if parsed:
                domain = parsed.domain.lower()
                if domain not in groups:
                    groups[domain] = []
                groups[domain].append(email)
        
        return groups

    @staticmethod
    def similar_emails(email: str, variations: List[str]) -> List[str]:
        """
        Find similar emails from a list (same domain or similar local part).

        Args:
            email: Reference email
            variations: List of emails to check

        Returns:
            List of similar emails

        Example:
            >>> EmailUtils.similar_emails("user@example.com", ["admin@example.com", "user@other.com"])
            ['admin@example.com', 'user@other.com']
        """
        parsed = EmailUtils.parse(email)
        if not parsed:
            return []
        
        similar = []
        for variant in variations:
            var_parsed = EmailUtils.parse(variant)
            if not var_parsed:
                continue
            
            # Same domain OR same local part
            if var_parsed.domain.lower() == parsed.domain.lower() or \
               var_parsed.local.lower() == parsed.local.lower():
                similar.append(variant)
        
        return similar


# Convenience functions for direct import

def validate(email: str) -> bool:
    """Validate an email address."""
    return EmailUtils.validate(email)


def parse(email: str) -> Optional[EmailAddress]:
    """Parse an email address into components."""
    return EmailUtils.parse(email)


def normalize(email: str) -> Optional[str]:
    """Normalize an email address."""
    return EmailUtils.normalize(email)


def is_disposable(email: str) -> bool:
    """Check if email is from a disposable provider."""
    return EmailUtils.is_disposable(email)


def is_free_provider(email: str) -> bool:
    """Check if email is from a free provider."""
    return EmailUtils.is_free_provider(email)


def get_domain(email: str) -> Optional[str]:
    """Extract domain from email."""
    return EmailUtils.get_domain(email)


def get_local(email: str) -> Optional[str]:
    """Extract local part from email."""
    return EmailUtils.get_local(email)


def obfuscate(email: str, show_chars: int = 2) -> Optional[str]:
    """Obfuscate email for display."""
    return EmailUtils.obfuscate(email, show_chars)


def format_with_name(email: str, name: Optional[str] = None) -> Optional[str]:
    """Format email with display name."""
    return EmailUtils.format_with_name(email, name)


def extract_from_text(text: str) -> List[str]:
    """Extract all emails from text."""
    return EmailUtils.extract_from_text(text)


def deduplicate(emails: List[str]) -> List[str]:
    """Remove duplicate emails."""
    return EmailUtils.deduplicate(emails)


def sort_by_domain(emails: List[str]) -> List[str]:
    """Sort emails by domain."""
    return EmailUtils.sort_by_domain(emails)


def group_by_domain(emails: List[str]) -> Dict[str, List[str]]:
    """Group emails by domain."""
    return EmailUtils.group_by_domain(emails)
