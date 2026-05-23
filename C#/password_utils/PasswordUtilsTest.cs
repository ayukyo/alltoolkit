using System;
using PasswordUtils;

namespace PasswordUtils.Tests
{
    /// <summary>
    /// Comprehensive tests for PasswordUtils
    /// Run with: dotnet run --project test-project
    /// Or compile and run directly with csc
    /// </summary>
    public class PasswordUtilsTest
    {
        private static int _passed = 0;
        private static int _failed = 0;

        public static void Main()
        {
            Console.WriteLine("=== PasswordUtils Test Suite ===\n");

            // Strength Analysis Tests
            TestAnalyzeStrength();
            
            // Password Generation Tests
            TestGenerate();
            TestGenerateMultiple();
            TestGeneratePassphrase();
            
            // Validation Tests
            TestIsCommonPassword();
            TestValidatePolicy();
            TestCalculateEntropy();
            
            // Edge Cases
            TestEdgeCases();

            // Summary
            Console.WriteLine("\n=== Test Summary ===");
            Console.WriteLine($"Passed: {_passed}");
            Console.WriteLine($"Failed: {_failed}");
            Console.WriteLine($"Total:  {_passed + _failed}");
            
            Environment.Exit(_failed > 0 ? 1 : 0);
        }

        static void TestAnalyzeStrength()
        {
            Console.WriteLine("--- Testing AnalyzeStrength ---");

            // Test empty password
            var emptyResult = PasswordUtils.AnalyzeStrength("");
            Assert(emptyResult.Strength == PasswordStrength.VeryWeak, "Empty password should be VeryWeak");
            Assert(emptyResult.Length == 0, "Empty password length should be 0");

            // Test common weak password
            var commonResult = PasswordUtils.AnalyzeStrength("password");
            Assert(commonResult.Strength == PasswordStrength.VeryWeak, "'password' should be VeryWeak");
            Assert(commonResult.Suggestions.Count > 0, "Weak password should have suggestions");

            // Test medium password
            var mediumResult = PasswordUtils.AnalyzeStrength("Password1");
            Assert(mediumResult.HasLowercase, "Should detect lowercase");
            Assert(mediumResult.HasUppercase, "Should detect uppercase");
            Assert(mediumResult.HasDigits, "Should detect digits");
            Assert(!mediumResult.HasSpecialChars, "Should not detect special chars");

            // Test strong password
            var strongResult = PasswordUtils.AnalyzeStrength("MyStr0ng!Pass#2024");
            Assert(strongResult.Strength >= PasswordStrength.Strong, "Complex password should be Strong");
            Assert(strongResult.HasSpecialChars, "Should detect special chars");
            Assert(strongResult.Entropy > 50, "Strong password should have high entropy");

            // Test very strong password
            var veryStrongResult = PasswordUtils.AnalyzeStrength("xK9#mP2$nL5@qR8&wT4!");
            Assert(veryStrongResult.Strength == PasswordStrength.VeryStrong, "Very complex password should be VeryStrong");
            Assert(veryStrongResult.Score >= 80, "VeryStrong password should have score >= 80");

            // Test keyboard pattern detection
            var patternResult = PasswordUtils.AnalyzeStrength("qwerty123!");
            Assert(patternResult.Score < 50, "Keyboard patterns should reduce score");

            // Test repeating chars detection
            var repeatResult = PasswordUtils.AnalyzeStrength("aaaAAA111!!!");
            Assert(repeatResult.Suggestions.Any(s => s.Contains("repeating")), 
                "Should suggest avoiding repeating chars");

            Console.WriteLine();
        }

        static void TestGenerate()
        {
            Console.WriteLine("--- Testing Generate ---");

            // Test default generation
            var password = PasswordUtils.Generate();
            Assert(password.Length == 16, "Default password should be 16 chars");
            Console.WriteLine($"  Generated: {password}");

            // Test custom length
            var shortPass = PasswordUtils.Generate(new PasswordOptions { Length = 8 });
            Assert(shortPass.Length == 8, "Custom length should be respected");

            var longPass = PasswordUtils.Generate(new PasswordOptions { Length = 32 });
            Assert(longPass.Length == 32, "Long password should be 32 chars");

            // Test character type inclusion
            var options = new PasswordOptions
            {
                Length = 20,
                IncludeLowercase = true,
                IncludeUppercase = true,
                IncludeDigits = true,
                IncludeSpecialChars = true
            };
            
            var complexPass = PasswordUtils.Generate(options);
            var analysis = PasswordUtils.AnalyzeStrength(complexPass);
            Assert(analysis.HasLowercase, "Should include lowercase");
            Assert(analysis.HasUppercase, "Should include uppercase");
            Assert(analysis.HasDigits, "Should include digits");
            Assert(analysis.HasSpecialChars, "Should include special chars");

            // Test exclude ambiguous
            var noAmbiguous = PasswordUtils.Generate(new PasswordOptions 
            { 
                Length = 20,
                ExcludeAmbiguous = true 
            });
            Assert(!noAmbiguous.Contains('l'), "Should exclude 'l' when ExcludeAmbiguous=true");
            Assert(!noAmbiguous.Contains('1'), "Should exclude '1' when ExcludeAmbiguous=true");
            Assert(!noAmbiguous.Contains('O'), "Should exclude 'O' when ExcludeAmbiguous=true");
            Assert(!noAmbiguous.Contains('0'), "Should exclude '0' when ExcludeAmbiguous=true");

            // Test custom characters
            var customPass = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 10,
                CustomChars = "abc123"
            });
            foreach (char c in customPass)
            {
                Assert("abc123".Contains(c), "Should only use custom chars");
            }

            // Test digits only
            var digitsOnly = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 6,
                IncludeLowercase = false,
                IncludeUppercase = false,
                IncludeDigits = true,
                IncludeSpecialChars = false
            });
            Assert(digitsOnly.All(char.IsDigit), "Should be digits only");

            Console.WriteLine();
        }

        static void TestGenerateMultiple()
        {
            Console.WriteLine("--- Testing GenerateMultiple ---");

            var passwords = PasswordUtils.GenerateMultiple(5);
            Assert(passwords.Count == 5, "Should generate 5 passwords");
            
            // Check uniqueness
            var uniquePasswords = passwords.Distinct().ToList();
            Assert(uniquePasswords.Count >= 4, "Most passwords should be unique (random generation)");

            // Test with options
            var customPasswords = PasswordUtils.GenerateMultiple(3, new PasswordOptions { Length = 12 });
            Assert(customPasswords.All(p => p.Length == 12), "All passwords should match custom length");

            Console.WriteLine("  Generated 5 passwords successfully\n");
        }

        static void TestGeneratePassphrase()
        {
            Console.WriteLine("--- Testing GeneratePassphrase ---");

            // Test default passphrase
            var passphrase = PasswordUtils.GeneratePassphrase();
            var words = passphrase.Split('-');
            Assert(words.Length == 4, "Default passphrase should have 4 words");
            Console.WriteLine($"  Generated: {passphrase}");

            // Test custom word count
            var shortPhrase = PasswordUtils.GeneratePassphrase(3);
            Assert(shortPhrase.Split('-').Length == 3, "Should have 3 words");

            // Test custom separator
            var spacePhrase = PasswordUtils.GeneratePassphrase(4, " ");
            Assert(spacePhrase.Split(' ').Length == 4, "Should use space separator");

            // Test capitalize
            var capPhrase = PasswordUtils.GeneratePassphrase(4, "-", true);
            var capWords = capPhrase.Split('-');
            Assert(capWords.All(w => char.IsUpper(w[0])), "All words should be capitalized");
            Console.WriteLine($"  Capitalized: {capPhrase}");

            // Test with number
            var numPhrase = PasswordUtils.GeneratePassphrase(4, "-", false, true);
            Assert(numPhrase.Any(char.IsDigit), "Should include a number");
            Console.WriteLine($"  With number: {numPhrase}");

            Console.WriteLine();
        }

        static void TestIsCommonPassword()
        {
            Console.WriteLine("--- Testing IsCommonPassword ---");

            // Test common passwords
            Assert(PasswordUtils.IsCommonPassword("password"), "'password' should be common");
            Assert(PasswordUtils.IsCommonPassword("123456"), "'123456' should be common");
            Assert(PasswordUtils.IsCommonPassword("qwerty"), "'qwerty' should be common");
            Assert(PasswordUtils.IsCommonPassword("PASSWORD"), "Should be case-insensitive");
            Assert(PasswordUtils.IsCommonPassword("Password123"), "Contains 'password' should be detected");

            // Test uncommon passwords
            Assert(!PasswordUtils.IsCommonPassword("xY7!kL9#mN2$"), "Complex password should not be common");
            Assert(!PasswordUtils.IsCommonPassword("uniquEPhrase42!"), "Unique password should not be common");

            Console.WriteLine("  All common password checks passed\n");
        }

        static void TestValidatePolicy()
        {
            Console.WriteLine("--- Testing ValidatePolicy ---");

            // Test valid password
            var (valid1, errors1) = PasswordUtils.ValidatePolicy("Password1!");
            Assert(valid1, "Should pass default policy");
            Assert(errors1.Count == 0, "Should have no errors");

            // Test too short
            var (valid2, errors2) = PasswordUtils.ValidatePolicy("Pass1!", minLength: 8);
            Assert(!valid2, "Should fail length requirement");
            Assert(errors2.Any(e => e.Contains("8 characters")), "Should mention length requirement");

            // Test missing uppercase
            var (valid3, errors3) = PasswordUtils.ValidatePolicy("password1!", requireUppercase: true);
            Assert(!valid3, "Should fail uppercase requirement");
            Assert(errors3.Any(e => e.Contains("uppercase")), "Should mention uppercase");

            // Test missing lowercase
            var (valid4, errors4) = PasswordUtils.ValidatePolicy("PASSWORD1!", requireLowercase: true);
            Assert(!valid4, "Should fail lowercase requirement");

            // Test missing digit
            var (valid5, errors5) = PasswordUtils.ValidatePolicy("Password!", requireDigit: true);
            Assert(!valid5, "Should fail digit requirement");

            // Test missing special
            var (valid6, errors6) = PasswordUtils.ValidatePolicy("Password1", requireSpecial: true);
            Assert(!valid6, "Should fail special char requirement");

            // Test multiple failures
            var (valid7, errors7) = PasswordUtils.ValidatePolicy("pass", minLength: 8, 
                requireUppercase: true, requireDigit: true, requireSpecial: true);
            Assert(!valid7, "Should fail multiple requirements");
            Assert(errors7.Count >= 3, "Should have multiple errors");

            Console.WriteLine("  All policy validation tests passed\n");
        }

        static void TestCalculateEntropy()
        {
            Console.WriteLine("--- Testing CalculateEntropy ---");

            // Test entropy calculation
            var entropy1 = PasswordUtils.CalculateEntropy("password");
            Assert(entropy1 > 0, "Should have entropy");

            var entropy2 = PasswordUtils.CalculateEntropy("Password");
            Assert(entropy2 > entropy1, "Mixed case should have higher entropy");

            var entropy3 = PasswordUtils.CalculateEntropy("Password1");
            Assert(entropy3 > entropy2, "With digits should have higher entropy");

            var entropy4 = PasswordUtils.CalculateEntropy("Password1!");
            Assert(entropy4 > entropy3, "With special chars should have highest entropy");

            // Test empty
            var entropyEmpty = PasswordUtils.CalculateEntropy("");
            Assert(entropyEmpty == 0, "Empty password should have 0 entropy");

            // Test long password
            var entropyLong = PasswordUtils.CalculateEntropy(new string('a', 100));
            Assert(entropyLong > 400, "Long password should have high entropy");

            Console.WriteLine($"  Entropy of 'Password1!': {entropy4:F2} bits\n");
        }

        static void TestEdgeCases()
        {
            Console.WriteLine("--- Testing Edge Cases ---");

            // Null/empty handling
            var nullAnalysis = PasswordUtils.AnalyzeStrength(null!);
            Assert(nullAnalysis.Strength == PasswordStrength.VeryWeak, "Null should be VeryWeak");

            // Single character
            var singleAnalysis = PasswordUtils.AnalyzeStrength("a");
            Assert(singleAnalysis.Length == 1, "Single char should work");
            Assert(singleAnalysis.Score < 20, "Single char should be VeryWeak");

            // Very long password
            var longPass = new string('x', 1000);
            var longAnalysis = PasswordUtils.AnalyzeStrength(longPass);
            Assert(longAnalysis.Length == 1000, "Should handle long passwords");

            // Unicode characters
            var unicodePass = "Pässwörd中文!🔥";
            var unicodeAnalysis = PasswordUtils.AnalyzeStrength(unicodePass);
            Assert(unicodeAnalysis.HasSpecialChars, "Unicode should count as special chars");

            // All same character
            var sameCharPass = "aaaaaaaaaaaa";
            var sameAnalysis = PasswordUtils.AnalyzeStrength(sameCharPass);
            Assert(sameAnalysis.Suggestions.Any(s => s.Contains("repeating")), 
                "Same char password should suggest no repeating");

            // Generate with all excludes
            var excludeAll = PasswordUtils.Generate(new PasswordOptions
            {
                Length = 20,
                IncludeLowercase = true,
                ExcludeAmbiguous = true,
                ExcludeSimilar = true
            });
            Assert(excludeAll.Length == 20, "Should handle excluded chars");

            // Passphrase edge cases
            var oneWord = PasswordUtils.GeneratePassphrase(1);
            Assert(oneWord.Split('-').Length == 1, "Should handle 1 word passphrase");

            Console.WriteLine("  All edge cases passed\n");
        }

        static void Assert(bool condition, string message)
        {
            if (condition)
            {
                Console.WriteLine($"  ✓ {message}");
                _passed++;
            }
            else
            {
                Console.WriteLine($"  ✗ FAILED: {message}");
                _failed++;
            }
        }
    }
}