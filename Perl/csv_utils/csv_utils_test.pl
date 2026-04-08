#!/usr/bin/perl
# CSV Utilities Test Suite
# Comprehensive tests for AllToolkit::CSVUtils

use strict;
use warnings;
use utf8;
use FindBin;
use lib $FindBin::Bin;
require "$FindBin::Bin/mod.pl";

my $TESTS_RUN = 0;
my $TESTS_PASSED = 0;
my $TESTS_FAILED = 0;

sub test {
    my ($name, $condition) = @_;
    $TESTS_RUN++;
    if ($condition) {
        $TESTS_PASSED++;
        print "[PASS] $name\n";
    } else {
        $TESTS_FAILED++;
        print "[FAIL] $name\n";
    }
}

sub test_eq {
    my ($name, $got, $expected) = @_;
    my $pass = defined($got) && defined($expected) && $got eq $expected;
    if (!$pass) {
        $got = 'undef' unless defined $got;
        $expected = 'undef' unless defined $expected;
    }
    test("$name (got: '$got', expected: '$expected')", $pass);
}

sub test_array_eq {
    my ($name, $got, $expected) = @_;
    my $pass = 1;
    if (!defined($got) || !defined($expected)) {
        $pass = 0;
    } elsif (@$got != @$expected) {
        $pass = 0;
    } else {
        for (my $i = 0; $i < @$got; $i++) {
            if (($got->[$i] // '') ne ($expected->[$i] // '')) {
                $pass = 0;
                last;
            }
        }
    }
    test($name, $pass);
}

print "=" x 60 . "\n";
print "CSV Utilities Test Suite\n";
print "=" x 60 . "\n\n";

#==============================================================================
# Test parse_csv
#==============================================================================
print "--- Testing parse_csv ---\n";

my $result = AllToolkit::CSVUtils::parse_csv('John,30,New York');
test_array_eq("Basic parsing", $result, ['John', '30', 'New York']);

$result = AllToolkit::CSVUtils::parse_csv('"John Doe",30,"New York, NY"');
test_array_eq("Quoted fields with commas", $result, ['John Doe', '30', 'New York, NY']);

$result = AllToolkit::CSVUtils::parse_csv('"John ""Johnny"" Doe",30');
test_array_eq("Escaped quotes", $result, ['John "Johnny" Doe', '30']);

$result = AllToolkit::CSVUtils::parse_csv('');
test_array_eq("Empty string", $result, ['']);

$result = AllToolkit::CSVUtils::parse_csv(undef);
test_array_eq("Undefined input", $result, []);

$result = AllToolkit::CSVUtils::parse_csv('a,b,c', { separator => "\t" });
test_array_eq("Tab separator (no match)", $result, ['a,b,c']);

$result = AllToolkit::CSVUtils::parse_csv("a\tb\tc", { separator => "\t" });
test_array_eq("Tab separator", $result, ['a', 'b', 'c']);

#==============================================================================
# Test parse_csv_string
#==============================================================================
print "\n--- Testing parse_csv_string ---\n";

$result = AllToolkit::CSVUtils::parse_csv_string("Name,Age\nJohn,30\nJane,25");
test_eq("Multi-line parsing rows", scalar(@$result), 3);
test_array_eq("First row", $result->[0], ['Name', 'Age']);
test_array_eq("Second row", $result->[1], ['John', '30']);

$result = AllToolkit::CSVUtils::parse_csv_string("Name,Age\r\nJohn,30\r\nJane,25");
test_eq("Windows line endings rows", scalar(@$result), 3);

$result = AllToolkit::CSVUtils::parse_csv_string("");
test_array_eq("Empty string", $result, []);

$result = AllToolkit::CSVUtils::parse_csv_string(undef);
test_array_eq("Undefined input", $result, []);

#==============================================================================
# Test parse_csv_with_headers
#==============================================================================
print "\n--- Testing parse_csv_with_headers ---\n";

my $hash_result = AllToolkit::CSVUtils::parse_csv_with_headers("Name,Age,City\nJohn,30,NYC\nJane,25,LA");
test_array_eq("Headers extracted", $hash_result->{headers}, ['Name', 'Age', 'City']);
test_eq("Row count", scalar(@{$hash_result->{rows}}), 2);
test_eq("First row Name", $hash_result->{rows}[0]{Name}, 'John');
test_eq("First row Age", $hash_result->{rows}[0]{Age}, '30');
test_eq("Second row City", $hash_result->{rows}[1]{City}, 'LA');

$hash_result = AllToolkit::CSVUtils::parse_csv_with_headers("");
test_array_eq("Empty string headers", $hash_result->{headers}, []);
test_array_eq("Empty string rows", $hash_result->{rows}, []);

#==============================================================================
# Test generate_csv
#==============================================================================
print "\n--- Testing generate_csv ---\n";

my $csv_line = AllToolkit::CSVUtils::generate_csv(['John', '30', 'New York']);
test_eq("Basic generation", $csv_line, 'John,30,New York');

$csv_line = AllToolkit::CSVUtils::generate_csv(['John, Doe', '30']);
test_eq("Field with comma", $csv_line, '"John, Doe",30');

$csv_line = AllToolkit::CSVUtils::generate_csv(['John "Johnny" Doe', '30']);
test_eq("Field with quotes", $csv_line, '"John ""Johnny"" Doe",30');

$csv_line = AllToolkit::CSVUtils::generate_csv(['John', '30'], { always_quote => 1 });
test_eq("Always quote", $csv_line, '"John","30"');

$csv_line = AllToolkit::CSVUtils::generate_csv([]);
test_eq("Empty array", $csv_line, '');

#==============================================================================
# Test generate_csv_string
#==============================================================================
print "\n--- Testing generate_csv_string ---\n";

my $csv_string = AllToolkit::CSVUtils::generate_csv_string([
    ['Name', 'Age'],
    ['John', '30'],
    ['Jane', '25']
]);
test_eq("Contains newline", index($csv_string, "\n") >= 0, 1);
test_eq("Ends with newline", substr($csv_string, -1), "\n");

#==============================================================================
# Test filter_rows
#==============================================================================
print "\n--- Testing filter_rows ---\n";

my $data = [
    ['John', '30'],
    ['Jane', '25'],
    ['Bob', '35']
];

my $filtered = AllToolkit::CSVUtils::filter_rows($data, sub {
    my $row = shift;
    return ($row->[1] // 0) >= 30;
});
test_eq("Filter >= 30 count", scalar(@$filtered), 2);
test_eq("First filtered name", $filtered->[0][0], 'John');

#==============================================================================
# Test filter_rows_hash
#==============================================================================
print "\n--- Testing filter_rows_hash ---\n";

my $hash_data = {
    headers => ['Name', 'Age'],
    rows => [
        { Name => 'John', Age => '30' },
        { Name => 'Jane', Age => '25' },
        { Name => 'Bob', Age => '35' }
    ]
};

my $filtered_hash = AllToolkit::CSVUtils::filter_rows_hash($hash_data, sub {
    my $row = shift;
    return ($row->{Age} // 0) >= 30;
});
test_eq("Filter hash >= 30 count", scalar(@{$filtered_hash->{rows}}), 2);

#==============================================================================
# Test get_column
#==============================================================================
print "\n--- Testing get_column ---\n";

my $column = AllToolkit::CSVUtils::get_column($data, 0);
test_array_eq("First column", $column, ['John', 'Jane', 'Bob']);

$column = AllToolkit::CSVUtils::get_column($data, 1);
test_array_eq("Second column", $column, ['30', '25', '35']);

#==============================================================================
# Test sort_by_column
#==============================================================================
print "\n--- Testing sort_by_column ---\n";

my $sorted = AllToolkit::CSVUtils::sort_by_column($data, 1, { numeric => 1 });
test_eq("Sort by age asc first", $sorted->[0][0], 'Jane');
test_eq("Sort by age asc last", $sorted->[2][0], 'Bob');

$sorted = AllToolkit::CSVUtils::sort_by_column($data, 1, { numeric => 1, reverse => 1 });
test_eq("Sort by age desc first", $sorted->[0][0], 'Bob');

#==============================================================================
# Test distinct_values
#==============================================================================
print "\n--- Testing distinct_values ---\n";

my $distinct_data = [
    ['A', '1'],
    ['B', '2'],
    ['A', '3'],
    ['C', '1']
];

my $distinct = AllToolkit::CSVUtils::distinct_values($distinct_data, 0);
test_array_eq("Distinct first column", $distinct, ['A', 'B', 'C']);

$distinct = AllToolkit::CSVUtils::distinct_values($distinct_data, 1);
test_array_eq("Distinct second column", $distinct, ['1', '2', '3']);

#==============================================================================
# Test is_valid_csv
#==============================================================================
print "\n--- Testing is_valid_csv ---\n";

test_eq("Valid CSV", AllToolkit::CSVUtils::is_valid_csv("Name,Age\nJohn,30"), 1);
test_eq("Valid empty", AllToolkit::CSVUtils::is_valid_csv(""), 1);
test_eq("Valid undef", AllToolkit::CSVUtils::is_valid_csv(undef), 0);

#==============================================================================
# Test count_rows
#==============================================================================
print "\n--- Testing count_rows ---\n";

test_eq("Count array rows", AllToolkit::CSVUtils::count_rows($data), 3);
test_eq("Count hash rows", AllToolkit::CSVUtils::count_rows($hash_data), 3);
test_eq("Count undef", AllToolkit::CSVUtils::count_rows(undef), 0);

#==============================================================================
# Test detect_separator
#==============================================================================
print "\n--- Testing detect_separator ---\n";

test_eq("Detect comma", AllToolkit::CSVUtils::detect_separator("a,b,c"), ',');
test_eq("Detect tab", AllToolkit::CSVUtils::detect_separator("a\tb\tc"), "\t");
test_eq("Detect semicolon", AllToolkit::CSVUtils::detect_separator("a;b;c;d"), ';');

#==============================================================================
# Test slice_rows
#==============================================================================
print "\n--- Testing slice_rows ---\n";

my $sliced = AllToolkit::CSVUtils::slice_rows($data, 0, 2);
test_eq("Slice 2 rows", scalar(@$sliced), 2);
test_eq("Slice first row", $sliced->[0][0], 'John');

$sliced = AllToolkit::CSVUtils::slice_rows($data, 1, 10);
test_eq("Slice with overflow", scalar(@$sliced), 2);

#==============================================================================
# Test merge_csv
#==============================================================================
print "\n--- Testing merge_csv ---\n";

my $data1 = {
    headers => ['Name', 'Age'],
    rows => [
        { Name => 'John', Age => '30' }
    ]
};

my $data2 = {
    headers => ['Name', 'City'],
    rows => [
        { Name => 'Jane', City => 'NYC' }
    ]
};

my $merged = AllToolkit::CSVUtils::merge_csv($data1, $data2);
test_array_eq("Merged headers", $merged->{headers}, ['Name', 'Age', 'City']);
test_eq("Merged row count", scalar(@{$merged->{rows}}), 2);
test_eq("Second row has City", $merged->{rows}[1]{City}, 'NYC');

#==============================================================================
# Summary
#==============================================================================
print "\n" . "=" x 60 . "\n";
print "Test Summary\n";
print "=" x 60 . "\n";
print "Tests run:    $TESTS_RUN\n";
print "Tests passed: $TESTS_PASSED\n";
print "Tests failed: $TESTS_FAILED\n";
print "Success rate: " . sprintf("%.1f%%", ($TESTS_PASSED / $TESTS_RUN * 100)) . "\n";
print "=" x 60 . "\n";

exit($TESTS_FAILED > 0 ? 1 : 0);