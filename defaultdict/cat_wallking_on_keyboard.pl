#!/usr/bin/env perl

use Data::Dumper;
my $data;
$data->{Will}[3]{this}[1][2]{work}[1]{Why}{Abuse}{Power}++;

print Dumper($data);
