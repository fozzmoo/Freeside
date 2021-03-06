package FS::m2m_Common;

use strict;
use vars qw( @ISA $DEBUG $me );
use FS::Schema qw( dbdef );
use FS::Record qw( qsearch qsearchs dbh );

#hmm.  well.  we seem to be used as a mixin.
#@ISA = qw( FS::Record );

$DEBUG = 0;
$me = '[FS::m2m_Common]';

=head1 NAME

FS::m2m_Common - Mixin class for classes in a many-to-many relationship

=head1 SYNOPSIS

use FS::m2m_Common;

@ISA = qw( FS::m2m_Common FS::Record );

=head1 DESCRIPTION

FS::m2m_Common is intended as a mixin class for classes which have a
many-to-many relationship with another table (via a linking table).

It is currently assumed that the link table contains two fields named the same
as the primary keys of the base and target tables, but you can ovverride this
assumption if your table is different.

=head1 METHODS

=over 4

=item process_m2m OPTION => VALUE, ...

Available options:

=over 4

=item link_table (required)

=item target_table (required)

=item params (required)

hashref; keys are primary key values in target_table (values are boolean).  For convenience, keys may optionally be prefixed with the name
of the primary key, as in "agentnum54" instead of "54", or passed as an arrayref
of values.

=item base_field (optional)

base field, defaults to primary key of this base table

=item target_field (optional)

target field, defaults to the primary key of the target table

=item hashref (optional)

static hashref further qualifying the m2m fields

=cut

sub process_m2m {
  my( $self, %opt ) = @_;

  #use Data::Dumper;
  #warn "$me process_m2m called on $self with options:\n". Dumper(%opt)
  warn "$me process_m2m called on $self"
    if $DEBUG;

  my $self_pkey = $self->dbdef_table->primary_key;
  my $base_field = $opt{'base_field'} || $self_pkey;
  my $hashref = $opt{'hashref'} || {};
  $hashref->{$base_field} = $self->$self_pkey();

  my $link_table = $self->_load_table($opt{'link_table'});

  my $target_table = $self->_load_table($opt{'target_table'});
  my $target_field = $opt{'target_field'}
                     || dbdef->table($target_table)->primary_key;

  if ( ref($opt{'params'}) eq 'ARRAY' ) {
    $opt{'params'} = { map { $_=>1 } @{$opt{'params'}} };
  }

  local $SIG{HUP} = 'IGNORE';
  local $SIG{INT} = 'IGNORE';
  local $SIG{QUIT} = 'IGNORE';
  local $SIG{TERM} = 'IGNORE';
  local $SIG{TSTP} = 'IGNORE';
  local $SIG{PIPE} = 'IGNORE';

  my $oldAutoCommit = $FS::UID::AutoCommit;
  local $FS::UID::AutoCommit = 0;
  my $dbh = dbh;

  foreach my $del_obj (
    grep { 
           my $targetnum = $_->$target_field();
           (    ! $opt{'params'}->{$targetnum}
             && ! $opt{'params'}->{"$target_field$targetnum"}
           );
         }
         qsearch( $link_table, $hashref )
  ) {
    my $error = $del_obj->delete;
    if ( $error ) {
      $dbh->rollback if $oldAutoCommit;
      return $error;
    }
  }

  foreach my $add_targetnum (
    grep { ! qsearchs( $link_table, { %$hashref, $target_field => $_ } ) }
    map  { /^($target_field)?(\d+)$/; $2; }
    grep { /^($target_field)?(\d+)$/ }
    grep { $opt{'params'}->{$_} }
    keys %{ $opt{'params'} }
  ) {

    my $add_obj = "FS::$link_table"->new( {
      %$hashref, 
      $target_field => $add_targetnum,
    });
    my $error = $add_obj->insert;
    if ( $error ) {
      $dbh->rollback if $oldAutoCommit;
      return $error;
    }
  }

  $dbh->commit or die $dbh->errstr if $oldAutoCommit;
  '';
}

sub _load_table {
  my( $self, $table ) = @_;
  eval "use FS::$table";
  die $@ if $@;
  $table;
}

#=item target_table
#
#=cut
#
#sub target_table {
#  my $self = shift;
#  my $target_table = $self->_target_table;
#  eval "use FS::$target_table";
#  die $@ if $@;
#  $target_table;
#}

=back

=head1 BUGS

=head1 SEE ALSO

L<FS::Record>

=cut

1;

