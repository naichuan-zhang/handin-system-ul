use strict;
use warnings FATAL => 'all';
while (<STDIN>)
{
    next if ! /^Found/;

    print $_;
}
