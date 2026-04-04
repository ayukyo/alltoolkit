using System;
using System.Collections.Generic;
using AllToolkit;

namespace AllToolkit.Examples
{
    /// <summary>
    /// Examples demonstrating EmailUtils functionality.
    /// </summary>
    class EmailUtilsExample
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== EmailUtils Examples ===");
            Console.WriteLine();

            Example1_BasicValidation();
            Example2_EmailTypes();
            Example3_Parsing();
            Example4_Formatting();
            Example5_Manipulation();
            Example6_BulkOperations();
            Example7_Generation();

            Console.WriteLine();
            Console.WriteLine("=== All examples completed ===");
        }

        static void Example1_BasicValidation()
        {
            Console.WriteLine("--- Example 1: Basic Validation ---");

            var emails = new[]
            {
                "user@example.com",
                "invalid.email",
                "test.user+tag@gmail.com",
                "@nodomain.com",
                "user@sub.domain.co.uk"
            };

            foreach (var email in emails)
            {
                var isValid = EmailUtils.IsValid(email);
                Console.WriteLine($"  {email} => {(isValid ? "Valid" : "Invalid")}");
            }

            Console.WriteLine();
        }

        static void Example2_EmailTypes()
        {
            Console.WriteLine("--- Example 2: Email Provider Types ---");

            var testEmails = new[]
            {
                "user@gmail.com",
                "user@company.com",
                "user@tempmail.com",
                "user@yahoo.com"
            };

            foreach (var email in testEmails)
            {
                var providerType = EmailUtils.GetProviderType(email);
                var isFree = EmailUtils.IsFreeProvider(email);
                var isBusiness = EmailUtils.IsBusinessEmail(email);
                var isDisposable = EmailUtils.IsDisposable(email);

                Console.WriteLine($"  {email}:");
                Console.WriteLine($"    Provider Type: {providerType}");
                Console.WriteLine($"    Free: {isFree}, Business: {isBusiness}, Disposable: {isDisposable}");
            }

            Console.WriteLine();
        }

        static void Example3_Parsing()
        {
            Console.WriteLine("--- Example 3: Parsing Email Parts ---");

            var email = "john.doe@example.com";
            var parts = EmailUtils.Parse(email);

            Console.WriteLine($"  Email: {email}");
            Console.WriteLine($"  Local Part: {parts.LocalPart}");
            Console.WriteLine($"  Domain: {parts.Domain}");
            Console.WriteLine($"  TLD: {parts.Tld}");

            // Direct extraction
            Console.WriteLine($"  Direct GetDomain: {EmailUtils.GetDomain(email)}");
            Console.WriteLine($"  Direct GetLocalPart: {EmailUtils.GetLocalPart(email)}");

            Console.WriteLine();
        }

        static void Example4_Formatting()
        {
            Console.WriteLine("--- Example 4: Formatting Emails ---");

            var email = "User@Example.COM";

            Console.WriteLine($"  Original: {email}");
            Console.WriteLine($"  Normalized: {EmailUtils.Normalize(email)}");
            Console.WriteLine($"  Lowercase: {EmailUtils.ToLower(email)}");
            Console.WriteLine($"  Masked: {EmailUtils.Mask("john.doe@example.com")}");
            Console.WriteLine($"  Masked (2 chars): {EmailUtils.Mask("john.doe@example.com", 2)}");
            Console.WriteLine($"  Display Name: {EmailUtils.ToDisplayName("john.doe@example.com")}");

            Console.WriteLine();
        }

        static void Example5_Manipulation()
        {
            Console.WriteLine("--- Example 5: Email Manipulation ---");

            var email = "user@example.com";

            Console.WriteLine($"  Original: {email}");
            Console.WriteLine($"  With plus tag: {EmailUtils.AddPlusTag(email, "newsletter")}");
            Console.WriteLine($"  Change domain: {EmailUtils.ChangeDomain(email, "newdomain.com")}");

            var taggedEmail = "user+oldtag@example.com";
            Console.WriteLine($"  Remove tag from {taggedEmail}: {EmailUtils.RemovePlusTag(taggedEmail)}");

            Console.WriteLine();
        }

        static void Example6_BulkOperations()
        {
            Console.WriteLine("--- Example 6: Bulk Operations ---");

            var emails = new List<string>
            {
                "alice@gmail.com",
                "bob@company.com",
                "charlie@gmail.com",
                "invalid-email",
                "diana@yahoo.com",
                "alice@gmail.com"  // duplicate
            };

            Console.WriteLine($"  Original list ({emails.Count} items):");
            emails.ForEach(e => Console.WriteLine($"    - {e}"));

            var valid = EmailUtils.FilterValid(emails);
            Console.WriteLine($"  Valid emails ({valid.Count}):");
            valid.ForEach(e => Console.WriteLine($"    - {e}"));

            var unique = EmailUtils.Deduplicate(emails);
            Console.WriteLine($"  Unique emails ({unique.Count}):");
            unique.ForEach(e => Console.WriteLine($"    - {e}"));

            var domains = EmailUtils.ExtractDomains(emails);
            Console.WriteLine($"  Unique domains ({domains.Count}): {string.Join(", ", domains)}");

            var grouped = EmailUtils.GroupByDomain(emails);
            Console.WriteLine("  Grouped by domain:");
            foreach (var group in grouped)
            {
                Console.WriteLine($"    {group.Key}: {string.Join(", ", group.Value)}");
            }

            Console.WriteLine();
        }

        static void Example7_Generation()
        {
            Console.WriteLine("--- Example 7: Email Generation ---");

            var randomEmail = EmailUtils.GenerateRandom();
            Console.WriteLine($"  Random email: {randomEmail}");

            var customRandom = EmailUtils.GenerateRandom("myapp.com", 12);
            Console.WriteLine($"  Custom random: {customRandom}");

            var testEmail = EmailUtils.GenerateTestEmail();
            Console.WriteLine($"  Test email: {testEmail}");

            var testEmail2 = EmailUtils.GenerateTestEmail("dev", "test.com");
            Console.WriteLine($"  Custom test email: {testEmail2}");

            Console.WriteLine();
        }
    }
}
