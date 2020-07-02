use warnings FATAL => 'all';
use strict;
while (<STDIN>)
{
    next if ! /^thread.*=.*(\d+)/;

    $threadUsed{$1}++;
}

(@threads) = sort {$a <=> $b} (keys %threadUsed);


$top = pop @threads;

print "$top\n";
