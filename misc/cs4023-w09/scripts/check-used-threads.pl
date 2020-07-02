use strict;
use warnings FATAL => 'all';
# make sure that the second file given, argv[1], has equal
#   thread used count and thread available count
# we have to ignore the class output (argv[0]) because it will
#   likely have been generated on a machine with a different no. of
#   processors and so there will be a mismatch between the two outputs
#   of 'count-used-threads.pl'.

my (@args) = @ARGV;

print "Examining $args[0] $args[1]...\n";
print "... but do we need $args[0] at all??\n";

my ($reported) = `grep -e '^Possible threads' $args[1]`;

die "Bad report..." unless ($reported =~ /^Possible threads: (\d+); used threads: (\d+)/);
my ($possible, $used) = ($1, $2);

if ($possible == $used)
{
    print "student used all\n";
    exit 0;
} else {
    print "student did not use all: $possible vs. $used\n";
    exit -1;
}
