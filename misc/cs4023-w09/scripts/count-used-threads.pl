use strict;
use warnings FATAL => 'all';
my (@processors) = `grep -e '^processor' /proc/cpuinfo`;
my ($pcount) = scalar @processors;

while (<STDIN>)
{
    next if ! /thread.*=\s*(\d+)/;

    $threadUsed{$1}++;
}

my (@threads) = sort {$a <=> $b} (keys %threadUsed);
my ($tcount) = scalar @threads;

print "Possible threads: $pcount; used threads: $tcount\n";
# print "All threads ", ($tcount == $pcount) ? "" : "not ", "used \n";

