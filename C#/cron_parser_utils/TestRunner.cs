using System;
using CronParserUtils.Tests;

// Simple test runner without dotnet
// Compile: csc CronExpression.cs CronDescriptor.cs CronExpressionTests.cs TestRunner.cs -out:Tests.exe
// Run: ./Tests.exe

class TestRunner
{
    static void Main()
    {
        CronExpressionTests.RunAllTests();
    }
}
