using System;
using PasswordUtils;

namespace PasswordUtils.Examples
{
    /// <summary>
    /// Usage examples for PasswordUtils
    /// Demonstrates all major features of the password utilities library.
    /// </summary>
    public class UsageExample
    {
        public static void Main()
        {
            Console.WriteLine("╔══════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║           PasswordUtils - Usage Examples                      ║");
            Console.WriteLine("╚══════════════════════════════════════════════════════════════╝\n");

            // 1. Password Strength Analysis
            AnalyzePasswordStrength();

            // 2. Password Generation
            GeneratePasswords();

            // 3. Passphrase Generation
            GeneratePassphrases();

            // 4. Password Validation
            ValidatePasswords();

            // 5. Entropy Calculation
            CalculateEntropyExamples();

            // 6. Common Password Detection
            DetectCommonPasswords();

            // 7. Rate Passwords
            RatePasswords();
        }

        static void AnalyzePasswordStrength()
        {
            PrintSection("Password Strength Analysis");

            string[] testPasswords = {
                "password",
                "Password1",
                "MySecureP@ss2024",
                "xK9#mP2$nL5@qR8&wT4!",
                "qwerty123"
            };

            foreach (var pwd in testPasswords)
            {
                var analysis = PasswordUtils.AnalyzeStrength(pwd);
                
                Console.WriteLine($"\nPassword: {pwd}");
                Console.WriteLine($"  Strength:     {analysis.Strength}");
                Console.WriteLine($"  Score:        {analysis.Score}/100");
                Console.WriteLine($"  Entropy:      {analysis.Entropy:F2} bits");
                Console.WriteLine($"  Crack Time:   {analysis.CrackTimeDisplay}");
                Console.WriteLine($"  Character Set:");
                Console.WriteLine($"    - Lowercase: {YesNo(analysis.HasLowercase)}");
                Console.WriteLine($"    - Uppercase: {YesNo(analysis.HasUppercase)}");
                Console.WriteLine($"    - Digits:    {YesNo(analysis.HasDigits)}");
                Console.WriteLine($"    - Special:   {YesNo(analysis.HasSpecialChars)}");
                
                if (analysis.Suggestions.Any())
                {
                    Console.WriteLine($"  Suggestions:");
                    foreach (var suggestion in analysis.Suggestions)
                    {
                        Console.WriteLine($"    → {suggestion}");
                    }
                }
            }
        }

        static void GeneratePasswords()
        {
            PrintSection("Password Generation");

            // Default generation
            Console.WriteLine("\n1. Default Password (16 chars, all character types):");
            for (int i = 0; i < 5; i++)
            {
                Console.WriteLine($"   {PasswordUtils.Generate()}");
            }

            // Custom length
            Console.WriteLine("\n2. Custom Length (8, 12, 24, 32 chars):");
            Console.WriteLine($"   8 chars:  {PasswordUtils.Generate(new PasswordOptions { Length = 8 })}");
            Console.WriteLine($"   12 chars: {PasswordUtils.Generate(new PasswordOptions { Length = 12 })}");
            Console.WriteLine($"   24 chars: {PasswordUtils.Generate(new PasswordOptions { Length = 24 })}");
            Console.WriteLine($"   32 chars: {PasswordUtils.Generate(new PasswordOptions { Length = 32 })}");

            // Exclude ambiguous characters
            Console.WriteLine("\n3. Exclude Ambiguous Characters (no l, 1, I, O, 0):");
            var noAmbiguous = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 16,
                ExcludeAmbiguous = true
            });
            Console.WriteLine($"   {noAmbiguous}");

            // Letters only
            Console.WriteLine("\n4. Letters Only:");
            var lettersOnly = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 12,
                IncludeLowercase = true,
                IncludeUppercase = true,
                IncludeDigits = false,
                IncludeSpecialChars = false
            });
            Console.WriteLine($"   {lettersOnly}");

            // PIN-style numeric
            Console.WriteLine("\n5. Numeric PIN (6 digits):");
            var pin = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 6,
                IncludeLowercase = false,
                IncludeUppercase = false,
                IncludeDigits = true,
                IncludeSpecialChars = false
            });
            Console.WriteLine($"   {pin}");

            // Custom character set
            Console.WriteLine("\n6. Custom Character Set (hexadecimal):");
            var hex = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 16,
                CustomChars = "0123456789ABCDEF"
            });
            Console.WriteLine($"   {hex}");

            // Generate multiple
            Console.WriteLine("\n7. Generate Multiple Passwords (10):");
            var passwords = PasswordUtils.GenerateMultiple(10, new PasswordOptions { Length = 12 });
            foreach (var p in passwords)
            {
                Console.WriteLine($"   {p}");
            }
        }

        static void GeneratePassphrases()
        {
            PrintSection("Passphrase Generation");

            // Default passphrase
            Console.WriteLine("\n1. Default Passphrase (4 words, '-' separator):");
            for (int i = 0; i < 3; i++)
            {
                Console.WriteLine($"   {PasswordUtils.GeneratePassphrase()}");
            }

            // Custom word count
            Console.WriteLine("\n2. 5 Words:");
            Console.WriteLine($"   {PasswordUtils.GeneratePassphrase(5)}");

            // Custom separator
            Console.WriteLine("\n3. Space Separator:");
            Console.WriteLine($"   {PasswordUtils.GeneratePassphrase(4, " ")}");

            // Capitalized
            Console.WriteLine("\n4. Capitalized Words:");
            Console.WriteLine($"   {PasswordUtils.GeneratePassphrase(4, "-", true)}");

            // With number
            Console.WriteLine("\n5. With Random Number:");
            Console.WriteLine($"   {PasswordUtils.GeneratePassphrase(4, "-", false, true)}");

            // Full options
            Console.WriteLine("\n6. Capitalized with Number:");
            Console.WriteLine($"   {PasswordUtils.GeneratePassphrase(5, ".", true, true)}");
        }

        static void ValidatePasswords()
        {
            PrintSection("Password Policy Validation");

            string[] testPasswords = {
                "weak",
                "Better123",
                "StrongP@ss!",
                "VeryStr0ng#Pass2024"
            };

            Console.WriteLine("\nValidating against policy (min 8 chars, 1 upper, 1 lower, 1 digit, 1 special):");
            
            foreach (var pwd in testPasswords)
            {
                var (isValid, errors) = PasswordUtils.ValidatePolicy(
                    pwd,
                    minLength: 8,
                    requireLowercase: true,
                    requireUppercase: true,
                    requireDigit: true,
                    requireSpecial: true
                );

                Console.WriteLine($"\nPassword: {pwd}");
                Console.WriteLine($"  Valid: {YesNo(isValid)}");
                
                if (errors.Any())
                {
                    Console.WriteLine("  Errors:");
                    foreach (var error in errors)
                    {
                        Console.WriteLine($"    ✗ {error}");
                    }
                }
            }
        }

        static void CalculateEntropyExamples()
        {
            PrintSection("Entropy Calculation");

            string[] passwords = {
                "password",
                "Password",
                "Password1",
                "Password1!",
                "MyV3ry$tr0ngP@ssw0rd!",
                "xK9#mP2$nL5@qR8&wT4!zY7%"
            };

            Console.WriteLine("\nEntropy comparison (higher is better):\n");
            Console.WriteLine($"{"Password",-30} {"Entropy (bits)",-15} {"Rating"}");
            Console.WriteLine(new string('-', 60));

            foreach (var pwd in passwords)
            {
                var entropy = PasswordUtils.CalculateEntropy(pwd);
                var rating = entropy switch
                {
                    < 28 => "Very Weak",
                    < 36 => "Weak",
                    < 60 => "Moderate",
                    < 80 => "Strong",
                    _ => "Very Strong"
                };
                Console.WriteLine($"{pwd,-30} {entropy,-15:F2} {rating}");
            }
        }

        static void DetectCommonPasswords()
        {
            PrintSection("Common Password Detection");

            string[] testPasswords = {
                "password",
                "123456",
                "qwerty",
                "letmein",
                "MyUniqueP@ss2024!",
                "xY7#kL9$mN2!",
                "admin",
                "password123"
            };

            Console.WriteLine("\nChecking for common passwords:\n");

            foreach (var pwd in testPasswords)
            {
                var isCommon = PasswordUtils.IsCommonPassword(pwd);
                var status = isCommon ? "⚠ COMMON" : "✓ Unique";
                Console.WriteLine($"  {pwd,-25} {status}");
            }
        }

        static void RatePasswords()
        {
            PrintSection("Password Rating (1-5 scale)");

            string[] testPasswords = {
                "a",
                "password",
                "Password1",
                "Password1!",
                "MyV3ry$tr0ngP@ssw0rd2024!"
            };

            Console.WriteLine("\nRating passwords on a scale of 1-5:\n");
            Console.WriteLine($"{"Password",-35} {"Rating"}");
            Console.WriteLine(new string('-', 50));

            foreach (var pwd in testPasswords)
            {
                var rating = PasswordUtils.RatePassword(pwd);
                var stars = new string('★', rating) + new string('☆', 5 - rating);
                Console.WriteLine($"{pwd,-35} {stars} ({rating}/5)");
            }
        }

        static void PrintSection(string title)
        {
            Console.WriteLine("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
            Console.WriteLine($"  {title}");
            Console.WriteLine("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        }

        static string YesNo(bool value) => value ? "✓ Yes" : "✗ No";
    }
}