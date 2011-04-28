package FS::part_event::Condition::billday;

use strict;
use Tie::IxHash;

use base qw( FS::part_event::Condition );

sub description {
  "Customer's monthly billing day is before or on current day or customer has no billing day";
}

sub condition {
  my( $self, $object ) = @_;

  my $cust_main = $self->cust_main($object);

  my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

  (!$cust_main->billday) || ($mday >= $cust_main->billday);
}

sub condition_sql {
  my( $self, $table ) = @_;

  my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

  "cust_main.billday is null or $mday >= cust_main.billday";
}

1;