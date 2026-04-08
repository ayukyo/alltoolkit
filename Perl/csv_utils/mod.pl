#!/usr/bin/perl
# CSV Utilities Module for Perl
# Provides comprehensive CSV parsing, generation, and manipulation
# Zero dependencies - uses only Perl standard library

package AllToolkit::CSVUtils;

use strict;
use warnings;
use utf8;

our $VERSION = '1.0.0';

# Default CSV options
our $DEFAULT_SEPARATOR = ',';
our $DEFAULT_QUOTE_CHAR = '"';
our $DEFAULT_NEWLINE = "\n";

#==============================================================================
# CSV Parsing Functions
#==============================================================================

sub parse_csv {
    my ($line, $options) = @_;
    return [] unless defined $line;
    
    $options ||= {};
    my $separator = $options->{separator} // $DEFAULT_SEPARATOR;
    my $quote_char = $options->{quote_char} // $DEFAULT_QUOTE_CHAR;
    
    chomp($line);
    my @fields;
    my $current_field = '';
    my $in_quotes = 0;
    my $i = 0;
    my $len = length($line);
    
    while ($i < $len) {
        my $char = substr($line, $i, 1);
        my $next_char = ($i + 1 < $len) ? substr($line, $i + 1, 1) : '';
        
        if ($char eq $quote_char) {
            if ($in_quotes) {
                if ($next_char eq $quote_char) {
                    $current_field .= $quote_char;
                    $i += 2;
                    next;
                } else {
                    $in_quotes = 0;
                }
            } else {
                $in_quotes = 1;
            }
        } elsif ($char eq $separator && !$in_quotes) {
            push @fields, $current_field;
            $current_field = '';
        } else {
            $current_field .= $char;
        }
        $i++;
    }
    
    push @fields, $current_field;
    return \@fields;
}

sub parse_csv_string {
    my ($csv_string, $options) = @_;
    return [] unless defined $csv_string && length($csv_string) > 0;
    
    my @lines = split(/\r?\n/, $csv_string);
    my @rows;
    
    foreach my $line (@lines) {
        next if $line eq '';
        push @rows, parse_csv($line, $options);
    }
    
    return \@rows;
}

sub parse_csv_with_headers {
    my ($csv_string, $options) = @_;
    return { headers => [], rows => [] } unless defined $csv_string;
    
    my $rows = parse_csv_string($csv_string, $options);
    return { headers => [], rows => [] } unless @$rows;
    
    my $headers = shift @$rows;
    my @data;
    
    foreach my $row (@$rows) {
        my %record;
        for (my $i = 0; $i < @$headers; $i++) {
            my $key = $headers->[$i];
            my $value = $i < @$row ? $row->[$i] : '';
            $record{$key} = $value;
        }
        push @data, \%record;
    }
    
    return {
        headers => $headers,
        rows => \@data
    };
}

sub read_csv_file {
    my ($filepath, $options) = @_;
    return undef unless defined $filepath && -f $filepath;
    
    $options ||= {};
    my $encoding = $options->{encoding} // 'utf8';
    my $has_headers = $options->{has_headers} // 1;
    
    open(my $fh, "<:encoding($encoding)", $filepath) or return undef;
    local $/;
    my $content = <$fh>;
    close($fh);
    
    return undef unless defined $content;
    
    if ($has_headers) {
        return parse_csv_with_headers($content, $options);
    } else {
        return parse_csv_string($content, $options);
    }
}

#==============================================================================
# CSV Generation Functions
#==============================================================================

sub generate_csv {
    my ($fields, $options) = @_;
    return '' unless defined $fields && @$fields;
    
    $options ||= {};
    my $separator = $options->{separator} // $DEFAULT_SEPARATOR;
    my $quote_char = $options->{quote_char} // $DEFAULT_QUOTE_CHAR;
    my $always_quote = $options->{always_quote} // 0;
    
    my @quoted_fields;
    
    foreach my $field (@$fields) {
        $field = '' unless defined $field;
        
        my $needs_quoting = $always_quote || 
                           ($field =~ /\Q$separator\E/) || 
                           ($field =~ /\Q$quote_char\E/) ||
                           ($field =~ /[\r\n]/);
        
        if ($needs_quoting) {
            my $escaped = $field;
            $escaped =~ s/\Q$quote_char\E/$quote_char$quote_char/g;
            $field = $quote_char . $escaped . $quote_char;
        }
        
        push @quoted_fields, $field;
    }
    
    return join($separator, @quoted_fields);
}

sub generate_csv_string {
    my ($rows, $options) = @_;
    return '' unless defined $rows && @$rows;
    
    my @lines;
    foreach my $row (@$rows) {
        push @lines, generate_csv($row, $options);
    }
    
    return join($DEFAULT_NEWLINE, @lines) . $DEFAULT_NEWLINE;
}

sub write_csv_file {
    my ($filepath, $data, $options) = @_;
    return 0 unless defined $filepath && defined $data;
    
    $options ||= {};
    my $encoding = $options->{encoding} // 'utf8';
    
    my $content;
    if (ref($data) eq 'ARRAY') {
        $content = generate_csv_string($data, $options);
    } elsif (ref($data) eq 'HASH' && exists $data->{rows}) {
        my @rows = ($data->{headers} // []);
        foreach my $row (@{$data->{rows}}) {
            my @fields;
            foreach my $header (@{$data->{headers}}) {
                push @fields, $row->{$header} // '';
            }
            push @rows, \@fields;
        }
        $content = generate_csv_string(\@rows, $options);
    } else {
        return 0;
    }
    
    open(my $fh, ">:encoding($encoding)", $filepath) or return 0;
    print $fh $content;
    close($fh);
    
    return 1;
}

#==============================================================================
# CSV Data Manipulation Functions
#==============================================================================

sub filter_rows {
    my ($data, $predicate) = @_;
    return [] unless defined $data && ref($data) eq 'ARRAY';
    return [] unless defined $predicate && ref($predicate) eq 'CODE';
    
    my @filtered;
    foreach my $row (@$data) {
        push @filtered, $row if $predicate->($row);
    }
    
    return \@filtered;
}

sub filter_rows_hash {
    my ($data, $predicate) = @_;
    return { headers => $data->{headers} // [], rows => [] } 
        unless defined $data && ref($data) eq 'HASH';
    return { headers => $data->{headers} // [], rows => [] } 
        unless defined $predicate && ref($predicate) eq 'CODE';
    
    my @filtered;
    foreach my $row (@{$data->{rows}}) {
        push @filtered, $row if $predicate->($row);
    }
    
    return {
        headers => $data->{headers},
        rows => \@filtered
    };
}

sub get_column {
    my ($data, $column_index) = @_;
    return [] unless defined $data && ref($data) eq 'ARRAY';
    
    my @values;
    foreach my $row (@$data) {
        push @values, $row->[$column_index] // '';
    }
    
    return \@values;
}

sub get_column_by_name {
    my ($data, $column_name) = @_;
    return [] unless defined $data && ref($data) eq 'HASH';
    return [] unless defined $column_name;
    
    my @values;
    foreach my $row (@{$data->{rows}}) {
        push @values, $row->{$column_name} // '';
    }
    
    return \@values;
}

sub sort_by_column {
    my ($data, $column_index, $options) = @_;
    return [] unless defined $data && ref($data) eq 'ARRAY';
    
    $options ||= {};
    my $numeric = $options->{numeric} // 0;
    my $reverse = $options->{reverse} // 0;
    
    my @sorted = @$data;
    
    if ($numeric) {
        @sorted = sort { 
            my $a_val = $a->[$column_index] // 0;
            my $b_val = $b->[$column_index] // 0;
            $a_val <=> $b_val 
        } @sorted;
    } else {
        @sorted = sort { 
            my $a_val = $a->[$column_index] // '';
            my $b_val = $b->[$column_index] // '';
            $a_val cmp $b_val 
        } @sorted;
    }
    
    @sorted = reverse @sorted if $reverse;
    return \@sorted;
}

sub sort_by_column_hash {
    my ($data, $column_name, $options) = @_;
    return { headers => $data->{headers} // [], rows => [] } 
        unless defined $data && ref($data) eq 'HASH';
    
    $options ||= {};
    my $numeric = $options->{numeric} // 0;
    my $reverse = $options->{reverse} // 0;
    
    my @sorted = @{$data->{rows}};
    
    if ($numeric) {
        @sorted = sort { 
            my $a_val = $a->{$column_name} // 0;
            my $b_val = $b->{$column_name} // 0;
            $a_val <=> $b_val 
        } @sorted;
    } else {
        @sorted = sort { 
            my $a_val = $a->{$column_name} // '';
            my $b_val = $b->{$column_name} // '';
            $a_val cmp $b_val 
        } @sorted;
    }
    
    @sorted = reverse @sorted if $reverse;
    
    return {
        headers => $data->{headers},
        rows => \@sorted
    };
}

sub distinct_values {
    my ($data, $column_index) = @_;
    return [] unless defined $data && ref($data) eq 'ARRAY';
    
    my %seen;
    my @distinct;
    
    foreach my $row (@$data) {
        my $value = $row->[$column_index] // '';
        unless ($seen{$value}) {
            $seen{$value} = 1;
            push @distinct, $value;
        }
    }
    
    return \@distinct;
}

sub distinct_values_by_name {
    my ($data, $column_name) = @_;
    return [] unless defined $data && ref($data) eq 'HASH';
    
    my %seen;
    my @distinct;
    
    foreach my $row (@{$data->{rows}}) {
        my $value = $row->{$column_name} // '';
        unless ($seen{$value}) {
            $seen{$value} = 1;
            push @distinct, $value;
        }
    }
    
    return \@distinct;
}

#==============================================================================
# CSV Validation and Utility Functions
#==============================================================================

sub is_valid_csv {
    my ($csv_string, $options) = @_;
    return 0 unless defined $csv_string;
    
    eval {
        my $rows = parse_csv_string($csv_string, $options);
        return 1;
    };
    
    return 0 if $@;
    return 1;
}

sub count_rows {
    my ($data) = @_;
    return 0 unless defined $data;
    
    if (ref($data) eq 'ARRAY') {
        return scalar(@$data);
    } elsif (ref($data) eq 'HASH' && exists $data->{rows}) {
        return scalar(@{$data->{rows}});
    }
    
    return 0;
}

sub get_headers {
    my ($data) = @_;
    return [] unless defined $data && ref($data) eq 'HASH';
    return $data->{headers} // [];
}

sub detect_separator {
    my ($csv_string) = @_;
    return ',' unless defined $csv_string;
    
    my %counts = (
        ',' => 0,
        "\t" => 0,
        ';' => 0,
        '|' => 0
    );
    
    foreach my $sep (keys %counts) {
        $counts{$sep} = () = $csv_string =~ /\Q$sep\E/g;
    }
    
    my $max_sep = ',';
    my $max_count = 0;
    
    foreach my $sep (keys %counts) {
        if ($counts{$sep} > $max_count) {
            $max_count = $counts{$sep};
            $max_sep = $sep;
        }
    }
    
    return $max_sep;
}

sub merge_csv {
    my ($data1, $data2, $options) = @_;
    return undef unless defined $data1 && defined $data2;
    return undef unless ref($data1) eq 'HASH' && ref($data2) eq 'HASH';
    
    my @headers = @{$data1->{headers} // []};
    my @rows = @{$data1->{rows} // []};
    
    # Add unique headers from data2
    my %header_map = map { $_ => 1 } @headers;
    foreach my $header (@{$data2->{headers} // []}) {
        unless ($header_map{$header}) {
            push @headers, $header;
            $header_map{$header} = 1;
        }
    }
    
    # Add rows from data2 with merged structure
    foreach my $row (@{$data2->{rows} // []}) {
        my %new_row;
        foreach my $header (@headers) {
            $new_row{$header} = $row->{$header} // '';
        }
        push @rows, \%new_row;
    }
    
    return {
        headers => \@headers,
        rows => \@rows
    };
}

sub slice_rows {
    my ($data, $start, $count) = @_;
    return [] unless defined $data && ref($data) eq 'ARRAY';
    
    $start //= 0;
    $count //= scalar(@$data);
    
    my $end = $start + $count;
    $end = scalar(@$data) if $end > scalar(@$data);
    
    my @sliced = @$data[$start..$end-1];
    return \@sliced;
}

sub slice_rows_hash {
    my ($data, $start, $count) = @_;
    return { headers => $data->{headers} // [], rows => [] } 
        unless defined $data && ref($data) eq 'HASH';
    
    $start //= 0;
    $count //= scalar(@{$data->{rows}});
    
    my $end = $start + $count;
    $end = scalar(@{$data->{rows}}) if $end > scalar(@{$data->{rows}});
    
    my @sliced = @{$data->{rows}}[$start..$end-1];
    
    return {
        headers => $data->{headers},
        rows => \@sliced
    };
}

#==============================================================================
# Export Functions
#==============================================================================

our @EXPORT_OK = qw(
    parse_csv parse_csv_string parse_csv_with_headers read_csv_file
    generate_csv generate_csv_string write_csv_file
    filter_rows filter_rows_hash get_column get_column_by_name
    sort_by_column sort_by_column_hash distinct_values distinct_values_by_name
    is_valid_csv count_rows get_headers detect_separator merge_csv
    slice_rows slice_rows_hash
);

our %EXPORT_TAGS = (
    all => \@EXPORT_OK,
    parse => [qw(parse_csv parse_csv_string parse_csv_with_headers read_csv_file)],
    generate => [qw(generate_csv generate_csv_string write_csv_file)],
    manipulate => [qw(filter_rows filter_rows_hash get_column get_column_by_name
                      sort_by_column sort_by_column_hash distinct_values distinct_values_by_name)],
    util => [qw(is_valid_csv count_rows get_headers detect_separator merge_csv
                slice_rows slice_rows_hash)]
);

1;

__END__

=head1 NAME

AllToolkit::CSVUtils - Comprehensive CSV Utilities for Perl

=head1 SYNOPSIS

    use AllToolkit::CSVUtils qw(:all);
    
    # Parse CSV string
    my $data = parse_csv_with_headers("Name,Age\nJohn,30\nJane,25");
    
    # Read from file
    my $csv = read_csv_file('data.csv', { has_headers => 1 });
    
    # Generate CSV
    my $csv_string = generate_csv_string([
        ['Name', 'Age'],
        ['John', '30'],
        ['Jane', '25']
    ]);
    
    # Write to file
    write_csv_file('output.csv', $csv);
    
    # Filter rows
    my $adults = filter_rows_hash($csv, sub {
        my $row = shift;
        return ($row->{Age} // 0) >= 18;
    });
    
    # Sort by column
    my $sorted = sort_by_column_hash($csv, 'Age', { numeric => 1 });

=head1 DESCRIPTION

AllToolkit::CSVUtils provides comprehensive CSV parsing, generation, and
manipulation functions with zero dependencies. It supports quoted fields,
different separators, and various data manipulation operations.

=head1 AUTHOR

AllToolkit Team

=head1 LICENSE

MIT License

=cut