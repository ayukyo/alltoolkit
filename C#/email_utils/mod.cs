using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Text.RegularExpressions;

namespace AllToolkit
{
    /// <summary>
    /// Email utilities for validation, parsing, formatting, and manipulation.
    /// Zero dependencies - uses only .NET standard library.
    /// </summary>
    public static class EmailUtils
    {
        // RFC 5322 compliant email pattern (simplified but comprehensive)
        private static readonly Regex EmailRegex = new Regex(
            @"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
            RegexOptions.Compiled | RegexOptions.IgnoreCase);

        // Strict email pattern for stricter validation
        private static readonly Regex StrictEmailRegex = new Regex(
            @"^(?![\x20-\x7f]*@[\x20-\x7f]*\.{2})[\x20-\x7f]+@[\x20-\x7f]+\.([a-zA-Z]{2,})$",
            RegexOptions.Compiled | RegexOptions.IgnoreCase);

        // Disposable email domains (common list)
        private static readonly HashSet<string> DisposableDomains = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "tempmail.com", "throwaway.com", "mailinator.com", "guerrillamail.com",
            "sharklasers.com", "spam4.me", "trashmail.com", "yopmail.com",
            "temp.inbox.com", "mailnesia.com", "tempmailaddress.com",
            "burnermail.io", "temp-mail.org", "fakeinbox.com", "getairmail.com",
            "10minutemail.com", "tempail.com", "throwawaymail.com"
        };

        // Common free email providers
        private static readonly HashSet<string> FreeEmailProviders = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com",
            "aol.com", "icloud.com", "mail.com", "protonmail.com", "zoho.com",
            "yandex.com", "qq.com", "163.com", "126.com", "sina.com",
            "foxmail.com", "sohu.com", "aliyun.com"
        };

        #region Validation

        /// <summary>
        /// Validates if the string is a valid email address format.
        /// </summary>
        /// <param name="email">The email address to validate.</param>
        /// <returns>True if valid email format, false otherwise.</returns>
        public static bool IsValid(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
                return false;

            email = email.Trim();

            if (email.Length > 254) // RFC 5321 limit
                return false;

            return EmailRegex.IsMatch(email);
        }

        /// <summary>
        /// Validates email with stricter rules (no consecutive dots, valid TLD, etc.).
        /// </summary>
        /// <param name="email">The email address to validate.</param>
        /// <returns>True if strictly valid, false otherwise.</returns>
        public static bool IsValidStrict(string email)
        {
            if (!IsValid(email))
                return false;

            email = email.Trim();

            // Check for consecutive dots
            if (email.Contains(".."))
                return false;

            // Check local part length (max 64)
            var localPart = email.Substring(0, email.IndexOf('@'));
            if (localPart.Length > 64)
                return false;

            // Check domain part
            var domain = email.Substring(email.IndexOf('@') + 1);
            if (domain.Length > 253)
                return false;

            // Check TLD (at least 2 chars)
            var tld = domain.Substring(domain.LastIndexOf('.') + 1);
            if (tld.Length < 2)
                return false;

            return StrictEmailRegex.IsMatch(email);
        }

        /// <summary>
        /// Validates email using .NET's MailAddress class.
        /// </summary>
        /// <param name="email">The email address to validate.</param>
        /// <returns>True if valid according to MailAddress, false otherwise.</returns>
        public static bool IsValidMailAddress(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
                return false;

            try
            {
                var addr = new MailAddress(email.Trim());
                return addr.Address == email.Trim();
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Checks if the email domain is a known disposable/temporary email provider.
        /// </summary>
        /// <param name="email">The email address to check.</param>
        /// <returns>True if disposable domain, false otherwise.</returns>
        public static bool IsDisposable(string email)
        {
            if (!IsValid(email))
                return false;

            var domain = GetDomain(email);
            return DisposableDomains.Contains(domain);
        }

        /// <summary>
        /// Checks if the email domain is a known free email provider.
        /// </summary>
        /// <param name="email">The email address to check.</param>
        /// <returns>True if free provider, false otherwise.</returns>
        public static bool IsFreeProvider(string email)
        {
            if (!IsValid(email))
                return false;

            var domain = GetDomain(email);
            return FreeEmailProviders.Contains(domain);
        }

        /// <summary>
        /// Checks if the email is likely a business/corporate email.
        /// </summary>
        /// <param name="email">The email address to check.</param>
        /// <returns>True if likely business email, false otherwise.</returns>
        public static bool IsBusinessEmail(string email)
        {
            if (!IsValid(email))
                return false;

            return !IsFreeProvider(email) && !IsDisposable(email);
        }

        #endregion

        #region Parsing

        /// <summary>
        /// Extracts the local part (username) from an email address.
        /// </summary>
        /// <param name="email">The email address.</param>
        /// <returns>The local part, or empty string if invalid.</returns>
        public static string GetLocalPart(string email)
        {
            if (!IsValid(email))
                return string.Empty;

            var atIndex = email.IndexOf('@');
            return atIndex > 0 ? email.Substring(0, atIndex).Trim() : string.Empty;
        }

        /// <summary>
        /// Extracts the domain from an email address.
        /// </summary>
        /// <param name="email">The email address.</param>
        /// <returns>The domain, or empty string if invalid.</returns>
        public static string GetDomain(string email)
        {
            if (!IsValid(email))
                return string.Empty;

            var atIndex = email.IndexOf('@');
            return atIndex >= 0 && atIndex < email.Length - 1 
                ? email.Substring(atIndex + 1).Trim().ToLowerInvariant() 
                : string.Empty;
        }

        /// <summary>
        /// Extracts the TLD (top-level domain) from an email address.
        /// </summary>
        /// <param name="email">The email address.</param>
        /// <returns>The TLD, or empty string if invalid.</returns>
        public static string GetTld(string email)
        {
            var domain = GetDomain(email);
            if (string.IsNullOrEmpty(domain))
                return string.Empty;

            var lastDot = domain.LastIndexOf('.');
            return lastDot >= 0 && lastDot < domain.Length - 1 
                ? domain.Substring(lastDot + 1).ToLowerInvariant() 
                : string.Empty;
        }

        /// <summary>
        /// Parses an email address into its components.
        /// </summary>
        /// <param name="email">The email address to parse.</param>
        /// <returns>EmailParts containing local, domain, and tld, or null if invalid.</returns>
        public static EmailParts Parse(string email)
        {
            if (!IsValid(email))
                return null;

            return new EmailParts
            {
                LocalPart = GetLocalPart(email),
                Domain = GetDomain(email),
                Tld = GetTld(email),
                Original = email.Trim()
            };
        }

        #endregion

        #region Formatting

        /// <summary>
        /// Normalizes an email address (lowercase domain, trim whitespace).
        /// </summary>
        /// <param name="email">The email address to normalize.</param>
        /// <returns>Normalized email, or empty string if invalid.</returns>
        public static string Normalize(string email)
        {
            if (!IsValid(email))
                return string.Empty;

            email = email.Trim();
            var atIndex = email.IndexOf('@');
            var local = email.Substring(0, atIndex);
            var domain = email.Substring(atIndex + 1).ToLowerInvariant();

            return $"{local}@{domain}";
        }

        /// <summary>
        /// Converts email to lowercase (entire address).
        /// </summary>
        /// <param name="email">The email address.</param>
        /// <returns>Lowercase email, or empty string if invalid.</returns>
        public static string ToLower(string email)
        {
            if (!IsValid(email))
                return string.Empty;

            return email.Trim().ToLowerInvariant();
        }

        /// <summary>
        /// Masks an email address for privacy (e.g., j***@example.com).
        /// </summary>
        /// <param name="email">The email address to mask.</param>
        /// <param name="visibleChars">Number of characters to show at start (default: 1).</param>
        /// <param name="maskChar">Character to use for masking (default: *).</param>
        /// <returns>Masked email, or empty string if invalid.</returns>
        public static string Mask(string email, int visibleChars = 1, char maskChar = '*')
        {
            if (!IsValid(email))
                return string.Empty;

            email = email.Trim();
            var local = GetLocalPart(email);
            var domain = GetDomain(email);

            if (local.Length <= visibleChars)
                return $"{local}@{domain}";

            var visible = local.Substring(0, visibleChars);
            var masked = new string(maskChar, Math.Min(local.Length - visibleChars, 3));
            return $"{visible}{masked}@{domain}";
        }

        /// <summary>
        /// Creates a display name from email (e.g., "john.doe" becomes "John Doe").
        /// </summary>
        /// <param name="email">The email address.</param>
        /// <returns>Formatted display name, or empty string if invalid.</returns>
        public static string ToDisplayName(string email)
        {
            var local = GetLocalPart(email);
            if (string.IsNullOrEmpty(local))
                return string.Empty;

            // Remove numbers and special chars, replace dots/underscores/hyphens with spaces
            var cleaned = Regex.Replace(local, @"[0-9]", "");
            cleaned = cleaned.Replace('.', ' ').Replace('_', ' ').Replace('-', ' ');
            cleaned = Regex.Replace(cleaned, @"\s+", " ").Trim();

            if (string.IsNullOrEmpty(cleaned))
                return local;

            // Title case
            var words = cleaned.Split(' ');
            var result = new StringBuilder();
            foreach (var word in words)
            {
                if (word.Length > 0)
                {
                    result.Append(char.ToUpperInvariant(word[0]));
                    if (word.Length > 1)
                        result.Append(word.Substring(1).ToLowerInvariant());
                    result.Append(' ');
                }
            }

            return result.ToString().Trim();
        }

        #endregion

        #region Manipulation

        /// <summary>
        /// Changes the domain of an email address.
        /// </summary>
        /// <param name="email">The original email.</param>
        /// <param name="newDomain">The new domain.</param>
        /// <returns>New email with changed domain, or empty string if invalid.</returns>
        public static string ChangeDomain(string email, string newDomain)
        {
            if (!IsValid(email) || string.IsNullOrWhiteSpace(newDomain))
                return string.Empty;

            var local = GetLocalPart(email);
            return $"{local}@{newDomain.Trim().ToLowerInvariant()}";
        }

        /// <summary>
        /// Generates a similar email with a plus suffix (e.g., user+tag@example.com).
        /// Works with Gmail and other providers supporting plus addressing.
        /// </summary>
        /// <param name="email">The base email.</param>
        /// <param name="tag">The tag to append.</param>
        /// <returns>Email with plus tag, or empty string if invalid.</returns>
        public static string AddPlusTag(string email, string tag)
        {
            if (!IsValid(email) || string.IsNullOrWhiteSpace(tag))
                return string.Empty;

            var local = GetLocalPart(email);
            var domain = GetDomain(email);

            // Remove existing plus tag if present
            var plusIndex = local.IndexOf('+');
            if (plusIndex >= 0)
                local = local.Substring(0, plusIndex);

            return $"{local}+{tag.Trim()}@{domain}";
        }

        /// <summary>
        /// Removes plus tag from email if present.
        /// </summary>
        /// <param name="email">The email with possible plus tag.</param>
        /// <returns>Email without plus tag, or empty string if invalid.</returns>
        public static string RemovePlusTag(string email)
        {
            if (!IsValid(email))
                return string.Empty;

            var local = GetLocalPart(email);
            var domain = GetDomain(email);

            var plusIndex = local.IndexOf('+');
            if (plusIndex >= 0)
                local = local.Substring(0, plusIndex);

            return $"{local}@{domain}";
        }

        /// <summary>
        /// Generates a random email address.
        /// </summary>
        /// <param name="domain">The domain to use (default: example.com).</param>
        /// <param name="length">Length of local part (default: 10).</param>
        /// <returns>Randomly generated email.</returns>
        public static string GenerateRandom(string domain = "example.com", int length = 10)
        {
            const string chars = "abcdefghijklmnopqrstuvwxyz0123456789";
            var random = new Random();
            var local = new StringBuilder(length);

            for (int i = 0; i < length; i++)
            {
                local.Append(chars[random.Next(chars.Length)]);
            }

            return $"{local}@{domain.Trim().ToLowerInvariant()}";
        }

        /// <summary>
        /// Generates a test email for development purposes.
        /// </summary>
        /// <param name="prefix">Prefix for the email (default: test).</param>
        /// <param name="domain">Domain to use (default: example.com).</param>
        /// <returns>Test email address.</returns>
        public static string GenerateTestEmail(string prefix = "test", string domain = "example.com")
        {
            var timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
            return $"{prefix.Trim().ToLowerInvariant()}.{timestamp}@{domain.Trim().ToLowerInvariant()}";
        }

        #endregion

        #region Bulk Operations

        /// <summary>
        /// Filters a list of emails, keeping only valid ones.
        /// </summary>
        /// <param name="emails">List of email addresses.</param>
        /// <returns>List of valid emails.</returns>
        public static List<string> FilterValid(IEnumerable<string> emails)
        {
            if (emails == null)
                return new List<string>();

            return emails.Where(e => IsValid(e)).Select(e => e.Trim()).ToList();
        }

        /// <summary>
        /// Removes duplicate emails (case-insensitive, normalizes domains).
        /// </summary>
        /// <param name="emails">List of email addresses.</param>
        /// <returns>List of unique normalized emails.</returns>
        public static List<string> Deduplicate(IEnumerable<string> emails)
        {
            if (emails == null)
                return new List<string>();

            var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            var result = new List<string>();

            foreach (var email in emails)
            {
                if (!IsValid(email))
                    continue;

                var normalized = Normalize(email);
                if (seen.Add(normalized))
                {
                    result.Add(normalized);
                }
            }

            return result;
        }

        /// <summary>
        /// Extracts unique domains from a list of emails.
        /// </summary>
        /// <param name="emails">List of email addresses.</param>
        /// <returns>List of unique domains.</returns>
        public static List<string> ExtractDomains(IEnumerable<string> emails)
        {
            if (emails == null)
                return new List<string>();

            var domains = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

            foreach (var email in emails)
            {
                var domain = GetDomain(email);
                if (!string.IsNullOrEmpty(domain))
                    domains.Add(domain);
            }

            return domains.ToList();
        }

        /// <summary>
        /// Groups emails by their domain.
        /// </summary>
        /// <param name="emails">List of email addresses.</param>
        /// <returns>Dictionary with domain as key and list of emails as value.</returns>
        public static Dictionary<string, List<string>> GroupByDomain(IEnumerable<string> emails)
        {
            var result = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);

            if (emails == null)
                return result;

            foreach (var email in emails)
            {
                if (!IsValid(email))
                    continue;

                var domain = GetDomain(email);
                if (!result.ContainsKey(domain))
                    result[domain] = new List<string>();

                result[domain].Add(email.Trim());
            }

            return result;
        }

        /// <summary>
        /// Sorts emails by domain, then by local part.
        /// </summary>
        /// <param name="emails">List of email addresses.</param>
        /// <returns>Sorted list of emails.</returns>
        public static List<string> SortByDomain(IEnumerable<string> emails)
        {
            if (emails == null)
                return new List<string>();

            return emails
                .Where(e => IsValid(e))
                .Select(e => new { Email = e.Trim(), Domain = GetDomain(e), Local = GetLocalPart(e) })
                .OrderBy(x => x.Domain)
                .ThenBy(x => x.Local)
                .Select(x => x.Email)
                .ToList();
        }

        #endregion

        #region Utility

        /// <summary>
        /// Checks if two emails are the same (case-insensitive, normalizes).
        /// </summary>
        /// <param name="email1">First email.</param>
        /// <param name="email2">Second email.</param>
        /// <returns>True if emails match, false otherwise.</returns>
        public static bool Equals(string email1, string email2)
        {
            if (email1 == null || email2 == null)
                return email1 == email2;

            var norm1 = Normalize(email1);
            var norm2 = Normalize(email2);

            return string.Equals(norm1, norm2, StringComparison.OrdinalIgnoreCase);
        }

        /// <summary>
        /// Gets the email provider type.
        /// </summary>
        /// <param name="email">The email address.</param>
        /// <returns>EmailProviderType enum value.</returns>
        public static EmailProviderType GetProviderType(string email)
        {
            if (!IsValid(email))
                return EmailProviderType.Unknown;

            if (IsDisposable(email))
                return EmailProviderType.Disposable;

            if (IsFreeProvider(email))
                return EmailProviderType.Free;

            return EmailProviderType.Business;
        }

        /// <summary>
        /// Adds a domain to the disposable email list.
        /// </summary>
        /// <param name="domain">Domain to add.</param>
        public static void AddDisposableDomain(string domain)
        {
            if (!string.IsNullOrWhiteSpace(domain))
                DisposableDomains.Add(domain.Trim().ToLowerInvariant());
        }

        /// <summary>
        /// Adds a domain to the free email provider list.
        /// </summary>
        /// <param name="domain">Domain to add.</param>
        public static void AddFreeProviderDomain(string domain)
        {
            if (!string.IsNullOrWhiteSpace(domain))
                FreeEmailProviders.Add(domain.Trim().ToLowerInvariant());
        }

        #endregion
    }

    /// <summary>
    /// Represents the parts of an email address.
    /// </summary>
    public class EmailParts
    {
        /// <summary>
        /// The local part (username) of the email.
        /// </summary>
        public string LocalPart { get; set; }

        /// <summary>
        /// The domain part of the email.
        /// </summary>
        public string Domain { get; set; }

        /// <summary>
        /// The top-level domain (e.g., com, org).
        /// </summary>
        public string Tld { get; set; }

        /// <summary>
        /// The original email address.
        /// </summary>
        public string Original { get; set; }

        /// <summary>
        /// Returns the full email address.
        /// </summary>
        public override string ToString()
        {
            return $"{LocalPart}@{Domain}";
        }
    }

    /// <summary>
    /// Types of email providers.
    /// </summary>
    public enum EmailProviderType
    {
        /// <summary>
        /// Unknown or invalid email.
        /// </summary>
        Unknown,

        /// <summary>
        /// Free email provider (Gmail, Yahoo, etc.).
        /// </summary>
        Free,

        /// <summary>
        /// Business/corporate email.
        /// </summary>
        Business,

        /// <summary>
        /// Disposable/temporary email.
        /// </summary>
        Disposable
    }
}
