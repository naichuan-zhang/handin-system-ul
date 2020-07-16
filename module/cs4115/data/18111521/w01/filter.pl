#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';

# get output and answer from ARGV
my ($output, $answer) = @ARGV;

if (not defined $output) {
    die "Need output\n";
}

if (defined $answer) {
    # replace numbers with a 'x' in a string
    $output =~ s/([0-9]+)/'x'/eg;
    $answer =~ s/([0-9]+)/'x'/eg;
    print("$output $answer");
}