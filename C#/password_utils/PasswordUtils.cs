using System;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Collections.Generic;

namespace PasswordUtils
{
    /// <summary>
    /// Password strength levels
    /// </summary>
    public enum PasswordStrength
    {
        VeryWeak = 0,
        Weak = 1,
        Fair = 2,
        Strong = 3,
        VeryStrong = 4
    }

    /// <summary>
    /// Result of password strength analysis
    /// </summary>
    public class PasswordAnalysis
    {
        public PasswordStrength Strength { get; set; }
        public double Entropy { get; set; }
        public int Length { get; set; }
        public bool HasLowercase { get; set; }
        public bool HasUppercase { get; set; }
        public bool HasDigits { get; set; }
        public bool HasSpecialChars { get; set; }
        public double CrackTimeSeconds { get; set; }
        public string CrackTimeDisplay { get; set; } = "";
        public List<string> Suggestions { get; set; } = new List<string>();
        public int Score { get; set; }
        public int MaxScore { get; set; } = 100;
    }

    /// <summary>
    /// Password generation options
    /// </summary>
    public class PasswordOptions
    {
        public int Length { get; set; } = 16;
        public bool IncludeLowercase { get; set; } = true;
        public bool IncludeUppercase { get; set; } = true;
        public bool IncludeDigits { get; set; } = true;
        public bool IncludeSpecialChars { get; set; } = true;
        public string? CustomChars { get; set; }
        public bool ExcludeAmbiguous { get; set; } = false;
        public bool ExcludeSimilar { get; set; } = false;
    }

    /// <summary>
    /// Comprehensive password utilities for strength checking, generation, and analysis.
    /// Zero external dependencies - uses only .NET standard library.
    /// </summary>
    public static class PasswordUtils
    {
        // Character sets for password generation
        private const string LowercaseChars = "abcdefghijklmnopqrstuvwxyz";
        private const string UppercaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        private const string DigitChars = "0123456789";
        private const string SpecialChars = "!@#$%^&*()_+-=[]{}|;:,.<>?";
        
        // Ambiguous characters (hard to distinguish)
        private const string AmbiguousChars = "l1IO0";
        
        // Similar characters
        private const string SimilarChars = "iIlL1oO0";

        // Common weak passwords (subset of rockyou.txt most common)
        private static readonly HashSet<string> CommonPasswords = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "password", "123456", "12345678", "qwerty", "abc123", "monkey", "master",
            "dragon", "111111", "baseball", "iloveyou", "trustno1", "sunshine",
            "princess", "welcome", "shadow", "superman", "michael", "football",
            "letmein", "password1", "password123", "admin", "login", "starwars",
            "passw0rd", "hello", "charlie", "donald", "lovely", "jessica",
            "ashley", "000000", "123123", "password1234", "qwerty123"
        };

        // Common keyboard patterns
        private static readonly string[] KeyboardPatterns = 
        {
            "qwerty", "asdfgh", "zxcvbn", "qwertyuiop", "asdfghjkl", "zxcvbnm",
            "1234567890", "qazwsx", "!@#$%^", "poiuyt", "lkjhgf", "mnbvcx"
        };

        /// <summary>
        /// Analyzes password strength and returns detailed analysis.
        /// </summary>
        /// <param name="password">The password to analyze</param>
        /// <returns>Detailed password analysis</returns>
        public static PasswordAnalysis AnalyzeStrength(string password)
        {
            var analysis = new PasswordAnalysis
            {
                Length = password.Length
            };

            if (string.IsNullOrEmpty(password))
            {
                analysis.Strength = PasswordStrength.VeryWeak;
                analysis.Entropy = 0;
                analysis.Suggestions.Add("Password cannot be empty");
                return analysis;
            }

            // Analyze character composition
            analysis.HasLowercase = password.Any(char.IsLower);
            analysis.HasUppercase = password.Any(char.IsUpper);
            analysis.HasDigits = password.Any(char.IsDigit);
            analysis.HasSpecialChars = password.Any(c => !char.IsLetterOrDigit(c));

            // Calculate charset size
            int charsetSize = 0;
            if (analysis.HasLowercase) charsetSize += 26;
            if (analysis.HasUppercase) charsetSize += 26;
            if (analysis.HasDigits) charsetSize += 10;
            if (analysis.HasSpecialChars) charsetSize += 32;

            // Calculate entropy
            analysis.Entropy = charsetSize > 0 
                ? password.Length * Math.Log2(charsetSize) 
                : 0;

            // Estimate crack time (assuming 10 billion attempts per second)
            double attemptsPerSecond = 10_000_000_000;
            double possibleCombinations = Math.Pow(charsetSize, password.Length);
            analysis.CrackTimeSeconds = possibleCombinations / attemptsPerSecond / 2; // Average case
            analysis.CrackTimeDisplay = FormatCrackTime(analysis.CrackTimeSeconds);

            // Calculate score (0-100)
            int score = 0;
            
            // Length scoring (up to 30 points)
            score += Math.Min(password.Length * 2, 30);
            
            // Character variety (up to 40 points)
            if (analysis.HasLowercase) score += 10;
            if (analysis.HasUppercase) score += 10;
            if (analysis.HasDigits) score += 10;
            if (analysis.HasSpecialChars) score += 10;
            
            // Entropy bonus (up to 30 points)
            score += Math.Min((int)(analysis.Entropy / 3), 30);

            // Penalties
            if (IsCommonPassword(password)) score -= 30;
            if (HasKeyboardPattern(password)) score -= 20;
            if (HasRepeatingChars(password)) score -= 10;
            if (HasSequentialChars(password)) score -= 10;

            score = Math.Max(0, Math.Min(100, score));
            analysis.Score = score;

            // Determine strength level
            analysis.Strength = DetermineStrength(score);

            // Generate suggestions
            GenerateSuggestions(analysis, password);

            return analysis;
        }

        /// <summary>
        /// Generates a secure random password.
        /// </summary>
        /// <param name="options">Password generation options</param>
        /// <returns>Generated password</returns>
        public static string Generate(PasswordOptions? options = null)
        {
            options ??= new PasswordOptions();
            
            var charPool = BuildCharPool(options);
            
            if (charPool.Length == 0)
            {
                throw new ArgumentException("At least one character type must be included");
            }

            var password = new StringBuilder();
            var requiredChars = new List<char>();

            // Ensure at least one character from each required set
            if (options.IncludeLowercase) requiredChars.Add(GetRandomChar(FilterChars(LowercaseChars, options)));
            if (options.IncludeUppercase) requiredChars.Add(GetRandomChar(FilterChars(UppercaseChars, options)));
            if (options.IncludeDigits) requiredChars.Add(GetRandomChar(FilterChars(DigitChars, options)));
            if (options.IncludeSpecialChars) requiredChars.Add(GetRandomChar(FilterChars(SpecialChars, options)));

            // Fill remaining length with random characters
            int remainingLength = options.Length - requiredChars.Count;
            for (int i = 0; i < remainingLength; i++)
            {
                password.Append(GetRandomChar(charPool));
            }

            // Insert required characters at random positions
            foreach (var c in requiredChars)
            {
                int pos = GetRandomInt(0, password.Length + 1);
                password.Insert(pos, c);
            }

            return password.ToString();
        }

        /// <summary>
        /// Generates multiple secure random passwords.
        /// </summary>
        /// <param name="count">Number of passwords to generate</param>
        /// <param name="options">Password generation options</param>
        /// <returns>List of generated passwords</returns>
        public static List<string> GenerateMultiple(int count, PasswordOptions? options = null)
        {
            var passwords = new List<string>();
            for (int i = 0; i < count; i++)
            {
                passwords.Add(Generate(options));
            }
            return passwords;
        }

        /// <summary>
        /// Generates a memorable passphrase using words.
        /// </summary>
        /// <param name="wordCount">Number of words in passphrase</param>
        /// <param name="separator">Word separator</param>
        /// <param name="capitalize">Whether to capitalize words</param>
        /// <param name="includeNumber">Whether to include a random number</param>
        /// <returns>Generated passphrase</returns>
        public static string GeneratePassphrase(int wordCount = 4, string separator = "-", 
            bool capitalize = false, bool includeNumber = false)
        {
            var words = GetWordList();
            var selectedWords = new List<string>();

            for (int i = 0; i < wordCount; i++)
            {
                string word = words[GetRandomInt(0, words.Count)];
                selectedWords.Add(capitalize ? Capitalize(word) : word);
            }

            string passphrase = string.Join(separator, selectedWords);

            if (includeNumber)
            {
                int pos = GetRandomInt(0, passphrase.Length);
                char num = DigitChars[GetRandomInt(0, DigitChars.Length)];
                passphrase = passphrase.Insert(pos, num.ToString());
            }

            return passphrase;
        }

        /// <summary>
        /// Checks if password is in common password list.
        /// </summary>
        /// <param name="password">Password to check</param>
        /// <returns>True if password is common</returns>
        public static bool IsCommonPassword(string password)
        {
            if (string.IsNullOrEmpty(password)) return false;
            
            // Check exact match
            if (CommonPasswords.Contains(password)) return true;
            
            // Check if password contains common password
            foreach (var common in CommonPasswords)
            {
                if (password.Length > common.Length && 
                    password.IndexOf(common, StringComparison.OrdinalIgnoreCase) >= 0)
                {
                    return true;
                }
            }
            
            return false;
        }

        /// <summary>
        /// Calculates the entropy of a password in bits.
        /// </summary>
        /// <param name="password">Password to analyze</param>
        /// <returns>Entropy in bits</returns>
        public static double CalculateEntropy(string password)
        {
            if (string.IsNullOrEmpty(password)) return 0;

            int charsetSize = 0;
            if (password.Any(char.IsLower)) charsetSize += 26;
            if (password.Any(char.IsUpper)) charsetSize += 26;
            if (password.Any(char.IsDigit)) charsetSize += 10;
            if (password.Any(c => !char.IsLetterOrDigit(c))) charsetSize += 32;

            return charsetSize > 0 ? password.Length * Math.Log2(charsetSize) : 0;
        }

        /// <summary>
        /// Gets a human-readable password strength label.
        /// </summary>
        /// <param name="password">Password to analyze</param>
        /// <returns>Strength label</returns>
        public static string GetStrengthLabel(string password)
        {
            var analysis = AnalyzeStrength(password);
            return analysis.Strength.ToString();
        }

        /// <summary>
        /// Validates password against common policy requirements.
        /// </summary>
        /// <param name="password">Password to validate</param>
        /// <param name="minLength">Minimum length requirement</param>
        /// <param name="requireLowercase">Require lowercase letter</param>
        /// <param name="requireUppercase">Require uppercase letter</param>
        /// <param name="requireDigit">Require digit</param>
        /// <param name="requireSpecial">Require special character</param>
        /// <returns>Validation result with messages</returns>
        public static (bool IsValid, List<string> Errors) ValidatePolicy(
            string password, 
            int minLength = 8,
            bool requireLowercase = true,
            bool requireUppercase = true,
            bool requireDigit = true,
            bool requireSpecial = false)
        {
            var errors = new List<string>();

            if (password.Length < minLength)
                errors.Add($"Password must be at least {minLength} characters long");

            if (requireLowercase && !password.Any(char.IsLower))
                errors.Add("Password must contain at least one lowercase letter");

            if (requireUppercase && !password.Any(char.IsUpper))
                errors.Add("Password must contain at least one uppercase letter");

            if (requireDigit && !password.Any(char.IsDigit))
                errors.Add("Password must contain at least one digit");

            if (requireSpecial && !password.Any(c => !char.IsLetterOrDigit(c)))
                errors.Add("Password must contain at least one special character");

            return (errors.Count == 0, errors);
        }

        /// <summary>
        /// Rates a password on a scale of 1-5.
        /// </summary>
        /// <param name="password">Password to rate</param>
        /// <returns>Rating from 1 (very weak) to 5 (very strong)</returns>
        public static int RatePassword(string password)
        {
            var analysis = AnalyzeStrength(password);
            return (int)analysis.Strength + 1;
        }

        #region Private Helper Methods

        private static PasswordStrength DetermineStrength(int score)
        {
            return score switch
            {
                < 20 => PasswordStrength.VeryWeak,
                < 40 => PasswordStrength.Weak,
                < 60 => PasswordStrength.Fair,
                < 80 => PasswordStrength.Strong,
                _ => PasswordStrength.VeryStrong
            };
        }

        private static void GenerateSuggestions(PasswordAnalysis analysis, string password)
        {
            if (analysis.Length < 12)
                analysis.Suggestions.Add("Use at least 12 characters");

            if (!analysis.HasLowercase)
                analysis.Suggestions.Add("Add lowercase letters");

            if (!analysis.HasUppercase)
                analysis.Suggestions.Add("Add uppercase letters");

            if (!analysis.HasDigits)
                analysis.Suggestions.Add("Add numbers");

            if (!analysis.HasSpecialChars)
                analysis.Suggestions.Add("Add special characters (!@#$%^&* etc.)");

            if (IsCommonPassword(password))
                analysis.Suggestions.Add("Avoid common passwords");

            if (HasKeyboardPattern(password))
                analysis.Suggestions.Add("Avoid keyboard patterns (qwerty, 123456)");

            if (HasRepeatingChars(password))
                analysis.Suggestions.Add("Avoid repeating characters");

            if (HasSequentialChars(password))
                analysis.Suggestions.Add("Avoid sequential characters (abc, 123)");
        }

        private static bool HasKeyboardPattern(string password)
        {
            string lower = password.ToLower();
            foreach (var pattern in KeyboardPatterns)
            {
                if (lower.Contains(pattern) || ContainsReverse(lower, pattern))
                    return true;
            }
            return false;
        }

        private static bool ContainsReverse(string text, string pattern)
        {
            string reversed = new string(pattern.Reverse().ToArray());
            return text.Contains(reversed);
        }

        private static bool HasRepeatingChars(string password)
        {
            for (int i = 0; i < password.Length - 2; i++)
            {
                if (password[i] == password[i + 1] && password[i + 1] == password[i + 2])
                    return true;
            }
            return false;
        }

        private static bool HasSequentialChars(string password)
        {
            for (int i = 0; i < password.Length - 2; i++)
            {
                if (IsSequential(password[i], password[i + 1], password[i + 2]))
                    return true;
            }
            return false;
        }

        private static bool IsSequential(char a, char b, char c)
        {
            return (a + 1 == b && b + 1 == c) || (a - 1 == b && b - 1 == c);
        }

        private static string FormatCrackTime(double seconds)
        {
            if (seconds < 1) return "Instant";
            if (seconds < 60) return $"{seconds:F0} seconds";
            if (seconds < 3600) return $"{seconds / 60:F0} minutes";
            if (seconds < 86400) return $"{seconds / 3600:F0} hours";
            if (seconds < 2592000) return $"{seconds / 86400:F0} days";
            if (seconds < 31536000) return $"{seconds / 2592000:F0} months";
            if (seconds < 3153600000) return $"{seconds / 31536000:F0} years";
            if (seconds < 3153600000000) return $"{seconds / 3153600000:F0} millennia";
            return "Centuries+";
        }

        private static string BuildCharPool(PasswordOptions options)
        {
            var pool = new StringBuilder();
            
            if (!string.IsNullOrEmpty(options.CustomChars))
            {
                return options.CustomChars;
            }

            if (options.IncludeLowercase) pool.Append(FilterChars(LowercaseChars, options));
            if (options.IncludeUppercase) pool.Append(FilterChars(UppercaseChars, options));
            if (options.IncludeDigits) pool.Append(FilterChars(DigitChars, options));
            if (options.IncludeSpecialChars) pool.Append(SpecialChars);

            return pool.ToString();
        }

        private static string FilterChars(string chars, PasswordOptions options)
        {
            if (!options.ExcludeAmbiguous && !options.ExcludeSimilar)
                return chars;

            var filtered = new StringBuilder();
            foreach (char c in chars)
            {
                if (options.ExcludeAmbiguous && AmbiguousChars.Contains(c))
                    continue;
                if (options.ExcludeSimilar && SimilarChars.Contains(c))
                    continue;
                filtered.Append(c);
            }
            return filtered.ToString();
        }

        private static char GetRandomChar(string chars)
        {
            return chars[GetRandomInt(0, chars.Length)];
        }

        private static int GetRandomInt(int min, int max)
        {
            byte[] bytes = new byte[4];
            RandomNumberGenerator.Fill(bytes);
            int value = BitConverter.ToInt32(bytes, 0);
            return Math.Abs(value % (max - min)) + min;
        }

        private static string Capitalize(string word)
        {
            if (string.IsNullOrEmpty(word)) return word;
            return char.ToUpper(word[0]) + word.Substring(1);
        }

        private static List<string> GetWordList()
        {
            // Common English words suitable for passphrases
            return new List<string>
            {
                "apple", "banana", "cherry", "dragon", "elephant", "forest",
                "garden", "harbor", "island", "jungle", "kitchen", "lemon",
                "mountain", "night", "ocean", "planet", "queen", "river",
                "sunset", "tiger", "umbrella", "valley", "water", "yellow",
                "zebra", "anchor", "bridge", "castle", "diamond", "eagle",
                "falcon", "guitar", "horizon", "insect", "jaguar", "knight",
                "library", "market", "notebook", "orange", "puzzle", "rabbit",
                "safari", "temple", "uniform", "violet", "window", "yellow",
                "adventure", "butterfly", "chocolate", "dinosaur", "element",
                "fantastic", "giraffe", "happiness", "internet", "journey",
                "keyboard", "language", "mystery", "notebook", "optimist",
                "paradise", "question", "rainbow", "sunshine", "treasure",
                "universe", "victory", "weather", "wonder", "yesterday"
            };
        }

        #endregion
    }
}