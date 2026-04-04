using System;
using System.Collections.Generic;
using System.Linq;

namespace AllToolkit.Tests
{
    public static class EmailUtilsTest
    {
        private static int _passed = 0;
        private static int _failed = 0;

        public static void Main(string[] args)
        {
            Console.WriteLine("=== EmailUtils Test Suite ===");
            Console.WriteLine();

            TestValidation();
            TestParsing();
            TestFormatting();
            TestManipulation();
            TestBulkOperations();
            TestUtility();

            Console.WriteLine();
            Console.WriteLine($"=== Results ===");
            Console.WriteLine($"Passed: {_passed}");
            Console.WriteLine($"Failed: {_failed}");
            Console.WriteLine($"Total: {_passed + _failed}");

            Environment.Exit(_failed > 0 ? 1 : 0);
        }

        private static void AssertTrue(bool condition, string testName)
        {
            if (condition)
            {
                Console.WriteLine($"  ✓ {testName}");
                _passed++;
            }
            else
            {
                Console.WriteLine($"  ✗ {testName}");
                _failed++;
            }
        }

        private static void AssertFalse(bool condition, string testName)
        {
            AssertTrue(!condition, testName);
        }

        private static void AssertEqual<T>(T expected, T actual, string testName)
        {
            AssertTrue(EqualityComparer<T>.Default.Equals(expected, actual), $"{testName} (expected: {expected}, got: {actual})");
        }

        private static void TestValidation()
        {
            Console.WriteLine("--- Validation Tests ---");

            AssertTrue(EmailUtils.IsValid("test@example.com"), "Valid simple email");
            AssertTrue(EmailUtils.IsValid("user.name@example.com"), "Valid email with dot");
            AssertTrue(EmailUtils.IsValid("user+tag@example.com"), "Valid email with plus");
            AssertTrue(EmailUtils.IsValid("user_name@example.com"), "Valid email with underscore");
            AssertTrue(EmailUtils.IsValid("user-name@example.com"), "Valid email with hyphen");
            AssertTrue(EmailUtils.IsValid("user@sub.example.com"), "Valid email with subdomain");
            AssertTrue(EmailUtils.IsValid("user@example.co.uk"), "Valid email with multi-level TLD");
            AssertTrue(EmailUtils.IsValid("User@Example.COM"), "Valid email with uppercase");

            AssertFalse(EmailUtils.IsValid(""), "Empty string is invalid");
            AssertFalse(EmailUtils.IsValid(null), "Null is invalid");
            AssertFalse(EmailUtils.IsValid("test"), "Missing @ is invalid");
            AssertFalse(EmailUtils.IsValid("test@"), "Missing domain is invalid");
            AssertFalse(EmailUtils.IsValid("@example.com"), "Missing local part is invalid");
            AssertFalse(EmailUtils.IsValid("test@@example.com"), "Double @ is invalid");
            AssertFalse(EmailUtils.IsValid("test@.com"), "Domain starting with dot is invalid");
            AssertFalse(EmailUtils.IsValid("test@example"), "Missing TLD is invalid");
            AssertFalse(EmailUtils.IsValid("test..name@example.com"), "Double dot in local is invalid");

            AssertTrue(EmailUtils.IsValidStrict("test@example.com"), "Strict valid email");
            AssertFalse(EmailUtils.IsValidStrict("test..name@example.com"), "Strict rejects consecutive dots");

            AssertTrue(EmailUtils.IsValidMailAddress("test@example.com"), "MailAddress valid email");
            AssertFalse(EmailUtils.IsValidMailAddress("invalid"), "MailAddress invalid email");

            AssertTrue(EmailUtils.IsDisposable("test@tempmail.com"), "Detects disposable domain");
            AssertFalse(EmailUtils.IsDisposable("test@gmail.com"), "Gmail is not disposable");

            AssertTrue(EmailUtils.IsFreeProvider("test@gmail.com"), "Gmail is free provider");
            AssertTrue(EmailUtils.IsFreeProvider("test@yahoo.com"), "Yahoo is free provider");
            AssertFalse(EmailUtils.IsFreeProvider("test@company.com"), "Company domain is not free");

            AssertTrue(EmailUtils.IsBusinessEmail("test@company.com"), "Company email is business");
            AssertFalse(EmailUtils.IsBusinessEmail("test@gmail.com"), "Gmail is not business");
            AssertFalse(EmailUtils.IsBusinessEmail("test@tempmail.com"), "Disposable is not business");

            Console.WriteLine();
        }

        private static void TestParsing()
        {
            Console.WriteLine("--- Parsing Tests ---");

            AssertEqual("test", EmailUtils.GetLocalPart("test@example.com"), "Extract local part");
            AssertEqual("user.name", EmailUtils.GetLocalPart("user.name@example.com"), "Extract local with dot");
            AssertEqual("", EmailUtils.GetLocalPart("invalid"), "Invalid email returns empty local");

            AssertEqual("example.com", EmailUtils.GetDomain("test@example.com"), "Extract domain");
            AssertEqual("sub.example.com", EmailUtils.GetDomain("test@sub.example.com"), "Extract subdomain");
            AssertEqual("", EmailUtils.GetDomain("invalid"), "Invalid email returns empty domain");

            AssertEqual("com", EmailUtils.GetTld("test@example.com"), "Extract TLD");
            AssertEqual("uk", EmailUtils.GetTld("test@example.co.uk"), "Extract multi-level TLD");

            var parts = EmailUtils.Parse("test@example.com");
            AssertTrue(parts != null, "Parse returns non-null");
            AssertEqual("test", parts.LocalPart, "Parse local part");
            AssertEqual("example.com", parts.Domain, "Parse domain");
            AssertEqual("com", parts.Tld, "Parse TLD");

            var nullParts = EmailUtils.Parse("invalid");
            AssertTrue(nullParts == null, "Parse invalid returns null");

            Console.WriteLine();
        }

        private static void TestFormatting()
        {
            Console.WriteLine("--- Formatting Tests ---");

            AssertEqual("test@example.com", EmailUtils.Normalize("test@EXAMPLE.COM"), "Normalize lowercase domain");
            AssertEqual("test@example.com", EmailUtils.Normalize("  test@example.com  "), "Normalize trims whitespace");

            AssertEqual("test@example.com", EmailUtils.ToLower("TEST@EXAMPLE.COM"), "ToLower entire email");

            AssertEqual("t***@example.com", EmailUtils.Mask("test@example.com"), "Mask with default params");
            AssertEqual("te**@example.com", EmailUtils.Mask("test@example.com", 2), "Mask with 2 visible chars");
            AssertEqual("t###@example.com", EmailUtils.Mask("test@example.com", 1, '#'), "Mask with custom char");
            AssertEqual("ab@example.com", EmailUtils.Mask("ab@example.com"), "Short local not masked");

            AssertEqual("Test", EmailUtils.ToDisplayName("test@example.com"), "Display name from simple email");
            AssertEqual("John Doe", EmailUtils.ToDisplayName("john.doe@example.com"), "Display name from dotted email");

            Console.WriteLine();
        }

        private static void TestManipulation()
        {
            Console.WriteLine("--- Manipulation Tests ---");

            AssertEqual("test@newdomain.com", EmailUtils.ChangeDomain("test@example.com", "newdomain.com"), "Change domain");
            AssertEqual("", EmailUtils.ChangeDomain("invalid", "newdomain.com"), "Change domain invalid email");

            AssertEqual("test+tag@example.com", EmailUtils.AddPlusTag("test@example.com", "tag"), "Add plus tag");
            AssertEqual("test+new@example.com", EmailUtils.AddPlusTag("test+old@example.com", "new"), "Replace plus tag");
            AssertEqual("test@example.com", EmailUtils.RemovePlusTag("test+tag@example.com"), "Remove plus tag");
            AssertEqual("test@example.com", EmailUtils.RemovePlusTag("test@example.com"), "Remove plus tag from clean email");

            var randomEmail = EmailUtils.GenerateRandom();
            AssertTrue(EmailUtils.IsValid(randomEmail), "Generated random email is valid");
            AssertTrue(randomEmail.EndsWith("@example.com"), "Random email uses default domain");

            var customRandom = EmailUtils.GenerateRandom("test.com", 8);
            AssertTrue(EmailUtils.IsValid(customRandom), "Custom random email is valid");
            AssertTrue(customRandom.EndsWith("@test.com"), "Custom random email uses custom domain");

            var testEmail = EmailUtils.GenerateTestEmail();
            AssertTrue(EmailUtils.IsValid(testEmail), "Generated test email is valid");
            AssertTrue(testEmail.StartsWith("test."), "Test email has prefix");

            Console.WriteLine();
        }

        private static void TestBulkOperations()
        {
            Console.WriteLine("--- Bulk Operations Tests ---");

            var emails = new List<string> { "a@example.com", "invalid", "b@example.com", "c@test.com", "a@example.com" };
            var valid = EmailUtils.FilterValid(emails);
            AssertEqual(4, valid.Count, "Filter valid returns 4 valid emails");

            var unique = EmailUtils.Deduplicate(emails);
            AssertEqual(3, unique.Count, "Deduplicate returns 3 unique emails");

            var domains = EmailUtils.ExtractDomains(emails);
            AssertEqual(2, domains.Count, "Extract domains returns 2 unique domains");

            var grouped = EmailUtils.GroupByDomain(emails);
            AssertEqual(2, grouped.Count, "Group by domain returns 2 groups");
            AssertEqual(2, grouped["example.com"].Count, "example.com group has 2 emails");

            var sorted = EmailUtils.SortByDomain(emails);
            AssertEqual("a@example.com", sorted[0], "Sort by domain first is example.com");

            Console.WriteLine();
        }

        private static void TestUtility()
        {
            Console.WriteLine("--- Utility Tests ---");

            AssertTrue(EmailUtils.Equals("test@example.com", "test@EXAMPLE.COM"), "Equals ignores case");
            AssertFalse(EmailUtils.Equals("test@example.com", "other@example.com"), "Different emails not equal");
            AssertTrue(EmailUtils.Equals(null, null), "Both null are equal");
            AssertFalse(EmailUtils.Equals("test@example.com", null), "Email vs null not equal");

            AssertEqual(EmailProviderType.Free, EmailUtils.GetProviderType("test@gmail.com"), "Gmail is free provider");
            AssertEqual(EmailProviderType.Business, EmailUtils.GetProviderType("test@company.com"), "Company is business");
            AssertEqual(EmailProviderType.Disposable, EmailUtils.GetProviderType("test@tempmail.com"), "Tempmail is disposable");
            AssertEqual(EmailProviderType.Unknown, EmailUtils.GetProviderType("invalid"), "Invalid is unknown");

            Console.WriteLine();
        }
    }
}
