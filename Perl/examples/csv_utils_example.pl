#!/usr/bin/perl
# CSV Utilities Example
# Demonstrates usage of AllToolkit::CSVUtils

use strict;
use warnings;
use utf8;
use FindBin;
use lib "$FindBin::Bin/../csv_utils";
use mod;

print "=" x 60 . "\n";
print "CSV Utilities Example\n";
print "=" x 60 . "\n\n";

#==============================================================================
# Example 1: Basic CSV Parsing
#==============================================================================
print "--- Example 1: Basic CSV Parsing ---\n";

my $csv_line = 'John Doe,30,"New York, NY",john@example.com';
my $fields = mod::parse_csv($csv_line);

print "Input: $csv_line\n";
print "Parsed fields:\n";
for (my $i = 0; $i < @$fields; $i++) {
    print "  [$i] = '$fields->[$i]'\n";
}

#==============================================================================
# Example 2: Parsing Multi-line CSV
#==============================================================================
print "\n--- Example 2: Parsing Multi-line CSV ---\n";

my $csv_data = <<'CSV';
Name,Age,Department,Salary
"John Doe",30,Engineering,75000
"Jane Smith",28,Marketing,65000
"Bob Johnson",35,"Sales, North",80000
"Alice Williams",32,Engineering,85000
CSV

my $rows = mod::parse_csv_string($csv_data);

print "Total rows: " . scalar(@$rows) . "\n";
print "First row (headers): " . join(', ', @{$rows->[0]}) . "\n";
print "Data rows:\n";
for (my $i = 1; $i < @$rows && $i <= 3; $i++) {
    print "  Row $i: " . join(' | ', @{$rows->[$i]}) . "\n";
}

#==============================================================================
# Example 3: CSV with Headers
#==============================================================================
print "\n--- Example 3: CSV with Headers ---\n";

my $csv_with_headers = <<'CSV';
Product,Price,Quantity,Category
Laptop,999.99,10,Electronics
Mouse,29.99,50,Electronics
Desk Chair,199.99,20,Furniture
Monitor,349.99,15,Electronics
CSV

my $parsed = mod::parse_csv_with_headers($csv_with_headers);

print "Headers: " . join(', ', @{$parsed->{headers}}) . "\n";
print "Products:\n";
foreach my $row (@{$parsed->{rows}}) {
    print "  - $row->{Product}: \$$row->{Price} ($row->{Quantity} in stock)\n";
}

#==============================================================================
# Example 4: Generating CSV
#==============================================================================
print "\n--- Example 4: Generating CSV ---\n";

my $output_rows = [
    ['Name', 'Email', 'Phone'],
    ['John Doe', 'john@example.com', '555-1234'],
    ['Jane Smith', 'jane@example.com', '555-5678'],
    ['Bob Johnson', 'bob@example.com', '555-9012']
];

my $generated_csv = mod::generate_csv_string($output_rows);
print "Generated CSV:\n$generated_csv";

#==============================================================================
# Example 5: Filtering Data
#==============================================================================
print "\n--- Example 5: Filtering Data ---\n";

my $sales_data = {
    headers => ['Product', 'Region', 'Sales'],
    rows => [
        { Product => 'Laptop', Region => 'North', Sales => '50000' },
        { Product => 'Mouse', Region => 'South', Sales => '15000' },
        { Product => 'Monitor', Region => 'North', Sales => '35000' },
        { Product => 'Keyboard', Region => 'East', Sales => '20000' },
        { Product => 'Laptop', Region => 'West', Sales => '45000' }
    ]
};

# Filter for North region only
my $north_sales = mod::filter_rows_hash($sales_data, sub {
    my $row = shift;
    return $row->{Region} eq 'North';
});

print "North Region Sales:\n";
foreach my $row (@{$north_sales->{rows}}) {
    print "  - $row->{Product}: \$$row->{Sales}\n";
}

# Filter for high sales (> 30000)
my $high_sales = mod::filter_rows_hash($sales_data, sub {
    my $row = shift;
    return ($row->{Sales} // 0) > 30000;
});

print "\nHigh Sales (>$30,000):\n";
foreach my $row (@{$high_sales->{rows}}) {
    print "  - $row->{Product} ($row->{Region}): \$$row->{Sales}\n";
}

#==============================================================================
# Example 6: Sorting Data
#==============================================================================
print "\n--- Example 6: Sorting Data ---\n";

my $employee_data = {
    headers => ['Name', 'Department', 'Salary'],
    rows => [
        { Name => 'John', Department => 'Engineering', Salary => '75000' },
        { Name => 'Jane', Department => 'Marketing', Salary => '65000' },
        { Name => 'Bob', Department => 'Sales', Salary => '80000' },
        { Name => 'Alice', Department => 'Engineering', Salary => '85000' }
    ]
};

# Sort by salary (numeric, ascending)
my $sorted_by_salary = mod::sort_by_column_hash($employee_data, 'Salary', { numeric => 1 });

print "Employees sorted by salary (ascending):\n";
foreach my $row (@{$sorted_by_salary->{rows}}) {
    print "  - $row->{Name}: \$$row->{Salary}\n";
}

# Sort by salary (numeric, descending)
my $sorted_desc = mod::sort_by_column_hash($employee_data, 'Salary', { numeric => 1, reverse => 1 });

print "\nEmployees sorted by salary (descending):\n";
foreach my $row (@{$sorted_desc->{rows}}) {
    print "  - $row->{Name}: \$$row->{Salary}\n";
}

#==============================================================================
# Example 7: Column Operations
#==============================================================================
print "\n--- Example 7: Column Operations ---\n";

my $product_data = [
    ['Product', 'Category', 'Price'],
    ['Laptop', 'Electronics', '999.99'],
    ['Mouse', 'Electronics', '29.99'],
    ['Desk', 'Furniture', '299.99'],
    ['Monitor', 'Electronics', '349.99']
];

# Get all categories
my $categories = mod::distinct_values($product_data, 1);
print "Unique categories: " . join(', ', @$categories) . "\n";

# Get all prices
my $prices = mod::get_column($product_data, 2);
print "All prices: " . join(', ', @$prices) . "\n";

#==============================================================================
# Example 8: Custom Separator (TSV)
#==============================================================================
print "\n--- Example 8: Custom Separator (TSV) ---\n";

my $tsv_data = "Name\tAge\tCity\nJohn\t30\tNYC\nJane\t25\tLA";
my $tsv_rows = mod::parse_csv_string($tsv_data, { separator => "\t" });

print "TSV Data:\n";
foreach my $row (@$tsv_rows) {
    print "  " . join(' | ', @$row) . "\n";
}

#==============================================================================
# Example 9: Writing CSV to File
#==============================================================================
print "\n--- Example 9: Writing CSV to File ---\n";

my $output_data = {
    headers => ['ID', 'Name', 'Score'],
    rows => [
        { ID => '1', Name => 'Alice', Score => '95' },
        { ID => '2', Name => 'Bob', Score => '87' },
        { ID => '3', Name => 'Charlie', Score => '92' }
    ]
};

my $temp_file = '/tmp/test_output.csv';
if (mod::write_csv_file($temp_file, $output_data)) {
    print "Successfully wrote CSV to $temp_file\n";
    
    # Read it back
    my $read_data = mod::read_csv_file($temp_file);
    if ($read_data) {
        print "Read back " . scalar(@{$read_data->{rows}}) . " rows\n";
    }
    unlink($temp_file);
} else {
    print "Failed to write CSV\n";
}

#==============================================================================
# Example 10: Data Slicing
#==============================================================================
print "\n--- Example 10: Data Slicing ---\n";

my $large_dataset = {
    headers => ['ID', 'Value'],
    rows => []
};

for (my $i = 1;
for (my $i = 1; $i <= 100; $i++) {
    push @{$large_dataset->{rows}}, { ID => $i, Value => "Value_$i" };
}

my $page1 = mod::slice_rows_hash($large_dataset, 0, 10);
my $page2 = mod::slice_rows_hash($large_dataset, 10, 10);

print "Total rows: " . mod::count_rows($large_dataset) . "\n";
print "Page 1 (rows 1-10): " . mod::count_rows($page1) . " rows\n";
print "  First: $page1->{rows}[0]{ID}, Last: $page1->{rows}[9]{ID}\n";
print "Page 2 (rows 11-20): " . mod::count_rows($page2) . " rows\n";
print "  First: $page2->{rows}[0]{ID}, Last: $page2->{rows}[9]{ID}\n";

#==============================================================================
# Summary
#==============================================================================
print "\n" . "=" x 60 . "\n";
print "All examples completed!\n";
print "=" x 60 . "\n";
