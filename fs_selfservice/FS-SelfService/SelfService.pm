package FS::SelfService;

use strict;
use vars qw($VERSION @ISA @EXPORT_OK $socket %autoload $tag);
use Exporter;
use Socket;
use FileHandle;
#use IO::Handle;
use IO::Select;
use Storable 2.09 qw(nstore_fd fd_retrieve);

$VERSION = '0.03';

@ISA = qw( Exporter );

$socket =  "/usr/local/freeside/selfservice_socket";
$socket .= '.'.$tag if defined $tag && length($tag);

#maybe should ask ClientAPI for this list
%autoload = (
  'passwd'               => 'passwd/passwd',
  'chfn'                 => 'passwd/passwd',
  'chsh'                 => 'passwd/passwd',
  'login'                => 'MyAccount/login',
  'logout'               => 'MyAccount/logout',
  'customer_info'        => 'MyAccount/customer_info',
  'edit_info'            => 'MyAccount/edit_info',     #add to ss cgi!
  'invoice'              => 'MyAccount/invoice',
  'list_invoices'        => 'MyAccount/list_invoices', #?
  'cancel'               => 'MyAccount/cancel',        #add to ss cgi!
  'payment_info'         => 'MyAccount/payment_info',
  'process_payment'      => 'MyAccount/process_payment',
  'list_pkgs'            => 'MyAccount/list_pkgs',     #add to ss cgi!
  'order_pkg'            => 'MyAccount/order_pkg',     #add to ss cgi!
  'cancel_pkg'           => 'MyAccount/cancel_pkg',    #add to ss cgi!
  'charge'               => 'MyAccount/charge',        #?
  'part_svc_info'        => 'MyAccount/part_svc_info',
  'provision_acct'       => 'MyAccount/provision_acct',
  'unprovision_svc'      => 'MyAccount/unprovision_svc',
  'signup_info'          => 'Signup/signup_info',
  'new_customer'         => 'Signup/new_customer',
  'agent_login'          => 'Agent/agent_login',
  'agent_info'           => 'Agent/agent_info',
  'agent_list_customers' => 'Agent/agent_list_customers',
);
@EXPORT_OK = ( keys(%autoload), qw( regionselector expselect popselector ) );

$ENV{'PATH'} ='/usr/bin:/usr/ucb:/bin';
$ENV{'SHELL'} = '/bin/sh';
$ENV{'IFS'} = " \t\n";
$ENV{'CDPATH'} = '';
$ENV{'ENV'} = '';
$ENV{'BASH_ENV'} = '';

my $freeside_uid = scalar(getpwnam('freeside'));
die "not running as the freeside user\n" if $> != $freeside_uid;

foreach my $autoload ( keys %autoload ) {

  my $eval =
  "sub $autoload { ". '
                   my $param;
                   if ( ref($_[0]) ) {
                     $param = shift;
                   } else {
                     $param = { @_ };
                   }

                   $param->{_packet} = \''. $autoload{$autoload}. '\';

                   simple_packet($param);
                 }';

  eval $eval;
  die $@ if $@;

}

sub simple_packet {
  my $packet = shift;
  socket(SOCK, PF_UNIX, SOCK_STREAM, 0) or die "socket: $!";
  connect(SOCK, sockaddr_un($socket)) or die "connect: $!";
  nstore_fd($packet, \*SOCK) or die "can't send packet: $!";
  SOCK->flush;

  #shoudl trap: Magic number checking on storable file failed at blib/lib/Storable.pm (autosplit into blib/lib/auto/Storable/fd_retrieve.al) line 337, at /usr/local/share/perl/5.6.1/FS/SelfService.pm line 71

  #block until there is a message on socket
#  my $w = new IO::Select;
#  $w->add(\*SOCK);
#  my @wait = $w->can_read;
  my $return = fd_retrieve(\*SOCK) or die "error reading result: $!";
  die $return->{'_error'} if defined $return->{_error} && $return->{_error};

  $return;
}

=head1 NAME

FS::SelfService - Freeside self-service API

=head1 SYNOPSIS

  # password and shell account changes
  use FS::SelfService qw(passwd chfn chsh);

  # "my account" functionality
  use FS::SelfService qw( login customer_info invoice cancel payment_info process_payment );

  my $rv = login( { 'username' => $username,
                    'domain'   => $domain,
                    'password' => $password,
                  }
                );

  if ( $rv->{'error'} ) {
    #handle login error...
  } else {
    #successful login
    my $session_id = $rv->{'session_id'};
  }

  my $customer_info = customer_info( { 'session_id' => $session_id } );

  #payment_info and process_payment are available in 1.5+ only
  my $payment_info = payment_info( { 'session_id' => $session_id } );

  #!!! process_payment example

  #!!! list_pkgs example

  #!!! order_pkg example

  #!!! cancel_pkg example

  # signup functionality
  use FS::SelfService qw( signup_info new_customer );

  my $signup_info = signup_info;

  $rv = new_customer( {
                        'first'            => $first,
                        'last'             => $last,
                        'company'          => $company,
                        'address1'         => $address1,
                        'address2'         => $address2,
                        'city'             => $city,
                        'state'            => $state,
                        'zip'              => $zip,
                        'country'          => $country,
                        'daytime'          => $daytime,
                        'night'            => $night,
                        'fax'              => $fax,
                        'payby'            => $payby,
                        'payinfo'          => $payinfo,
                        'paycvv'           => $paycvv,
                        'paydate'          => $paydate,
                        'payname'          => $payname,
                        'invoicing_list'   => $invoicing_list,
                        'referral_custnum' => $referral_custnum,
                        'pkgpart'          => $pkgpart,
                        'username'         => $username,
                        '_password'        => $password,
                        'popnum'           => $popnum,
                        'agentnum'         => $agentnum,
                      }
                    );
  
  my $error = $rv->{'error'};
  if ( $error eq '_decline' ) {
    print_decline();
  } elsif ( $error ) {
    reprint_signup();
  } else {
    print_success();
  }

=head1 DESCRIPTION

Use this API to implement your own client "self-service" module.

If you just want to customize the look of the existing "self-service" module,
see XXXX instead.

=head1 PASSWORD, GECOS, SHELL CHANGING FUNCTIONS

=over 4

=item passwd

=item chfn

=item chsh

=back

=head1 "MY ACCOUNT" FUNCTIONS

=over 4

=item login HASHREF

Creates a user session.  Takes a hash reference as parameter with the
following keys:

=over 4

=item username

=item domain

=item password

=back

Returns a hash reference with the following keys:

=over 4

=item error

Empty on success, or an error message on errors.

=item session_id

Session identifier for successful logins

=back

=item customer_info HASHREF

Returns general customer information.

Takes a hash reference as parameter with a single key: B<session_id>

Returns a hash reference with the following keys:

=over 4

=item name

Customer name

=item balance

Balance owed

=item open

Array reference of hash references of open inoices.  Each hash reference has
the following keys: invnum, date, owed

=item small_custview

An HTML fragment containing shipping and billing addresses.

=item The following fields are also returned: first last company address1 address2 city county state zip country daytime night fax ship_first ship_last ship_company ship_address1 ship_address2 ship_city ship_state ship_zip ship_country ship_daytime ship_night ship_fax payby payinfo payname month year invoicing_list postal_invoicing

=back

=item edit_info HASHREF

Takes a hash reference as parameter with any of the following keys:

first last company address1 address2 city county state zip country daytime night fax ship_first ship_last ship_company ship_address1 ship_address2 ship_city ship_state ship_zip ship_country ship_daytime ship_night ship_fax payby payinfo paycvv payname month year invoicing_list postal_invoicing

If a field exists, the customer record is updated with the new value of that
field.  If a field does not exist, that field is not changed on the customer
record.

Returns a hash reference with a single key, B<error>, empty on success, or an
error message on errors

=item invoice HASHREF

Returns an invoice.  Takes a hash reference as parameter with two keys:
session_id and invnum

Returns a hash reference with the following keys:

=over 4

=item error

Empty on success, or an error message on errors

=item invnum

Invoice number

=item invoice_text

Invoice text

=back

=item list_invoices HASHREF

Returns a list of all customer invoices.  Takes a hash references with a single
key, session_id.

Returns a hash reference with the following keys:

=over 4

=item error

Empty on success, or an error message on errors

=item invoices

Reference to array of hash references with the following keys:

=over 4

=item invnum

Invoice ID

=item _date

Invoice date, in UNIX epoch time

=back

=back

=item cancel HASHREF

Cancels this customer.

Takes a hash reference as parameter with a single key: B<session_id>

Returns a hash reference with a single key, B<error>, which is empty on
success or an error message on errors.

=item payment_info HASHREF

Returns information that may be useful in displaying a payment page.

Takes a hash reference as parameter with a single key: B<session_id>.

Returns a hash reference with the following keys:

=over 4

=item error

Empty on success, or an error message on errors

=item balance

Balance owed

=item payname

Exact name on credit card (CARD/DCRD)

=item address1

=item address2

=item city

=item state

=item zip

=item payby

Customer's current default payment type.

=item card_type

For CARD/DCRD payment types, the card type (Visa card, MasterCard, Discover card, American Express card, etc.)

=item payinfo

For CARD/DCRD payment types, the card number

=item month

For CARD/DCRD payment types, expiration month

=item year

For CARD/DCRD payment types, expiration year

=item cust_main_county

County/state/country data - array reference of hash references, each of which has the fields of a cust_main_county record (see L<FS::cust_main_county>).  Note these are not FS::cust_main_county objects, but hash references of columns and values.

=item states

Array reference of all states in the current default country.

=item card_types

Hash reference of card types; keys are card types, values are the exact strings
passed to the process_payment function

=item paybatch

Unique transaction identifier (prevents multiple charges), passed to the
process_payment function

=back

=item process_payment HASHREF

Processes a payment and possible change of address or payment type.  Takes a
hash reference as parameter with the following keys:

=over 4

=item session_id

=item save

If true, address and card information entered will be saved for subsequent
transactions.

=item auto

If true, future credit card payments will be done automatically (sets payby to
CARD).  If false, future credit card payments will be done on-demand (sets
payby to DCRD).  This option only has meaning if B<save> is set true.  

=item payname

=item address1

=item address2

=item city

=item state

=item zip

=item payinfo

Card number

=item month

Card expiration month

=item year

Card expiration year

=item paybatch

Unique transaction identifier, returned from the payment_info function.
Prevents multiple charges.

=back

Returns a hash reference with a single key, B<error>, empty on success, or an
error message on errors

=item list_pkgs

Returns package information for this customer.

Takes a hash reference as parameter with a single key: B<session_id>

Returns a hash reference containing customer package information.  The hash reference contains the following keys:

=over 4


=item cust_pkg HASHREF

Array reference of hash references, each of which has the fields of a cust_pkg
record (see L<FS::cust_pkg>) as well as the fields below.  Note these are not
the internal FS:: objects, but hash references of columns and values.

=item all fields of part_pkg (XXXpare this down to a secure subset)

=item part_svc - An array of hash references, each of which has the following keys:

=over 4

=item all fields of part_svc (XXXpare this down to a secure subset)

=item avail

=back

=item error

Empty on success, or an error message on errors.

=back

=item order_pkg

Orders a package for this customer.

Takes a hash reference as parameter with the following keys:

=over 4

=item session_id

=item pkgpart

=item svcpart

optional svcpart, required only if the package definition does not contain
one svc_acct service definition with quantity 1 (it may contain others with
quantity >1)

=item username

=item _password

=item sec_phrase

=item popnum

=back

Returns a hash reference with a single key, B<error>, empty on success, or an
error message on errors.  The special error '_decline' is returned for
declined transactions.

=item cancel_pkg

Cancels a package for this customer.

Takes a hash reference as parameter with the following keys:

=over 4

=item session_id

=item pkgpart

=back

Returns a hash reference with a single key, B<error>, empty on success, or an
error message on errors.

=back

=head1 SIGNUP FUNCTIONS

=over 4

=item signup_info HASHREF

Takes a hash reference as parameter with the following keys:

=over 4

=item session_id - Optional agent/reseller interface session

=back

Returns a hash reference containing information that may be useful in
displaying a signup page.  The hash reference contains the following keys:

=over 4

=item cust_main_county

County/state/country data - array reference of hash references, each of which has the fields of a cust_main_county record (see L<FS::cust_main_county>).  Note these are not FS::cust_main_county objects, but hash references of columns and values.

=item part_pkg

Available packages - array reference of hash references, each of which has the fields of a part_pkg record (see L<FS::part_pkg>).  Each hash reference also has an additional 'payby' field containing an array reference of acceptable payment types specific to this package (see below and L<FS::part_pkg/payby>).  Note these are not FS::part_pkg objects, but hash references of columns and values.  Requires the 'signup_server-default_agentnum' configuration value to be set, or
an agentnum specified explicitly via reseller interface session_id in the
options.

=item agent

Array reference of hash references, each of which has the fields of an agent record (see L<FS::agent>).  Note these are not FS::agent objects, but hash references of columns and values.

=item agentnum2part_pkg

Hash reference; keys are agentnums, values are array references of available packages for that agent, in the same format as the part_pkg arrayref above.

=item svc_acct_pop

Access numbers - array reference of hash references, each of which has the fields of an svc_acct_pop record (see L<FS::svc_acct_pop>).  Note these are not FS::svc_acct_pop objects, but hash references of columns and values.

=item security_phrase

True if the "security_phrase" feature is enabled

=item payby

Array reference of acceptable payment types for signup

=over 4

=item CARD (credit card - automatic)

=item DCRD (credit card - on-demand - version 1.5+ only)

=item CHEK (electronic check - automatic)

=item DCHK (electronic check - on-demand - version 1.5+ only)

=item LECB (Phone bill billing)

=item BILL (billing, not recommended for signups)

=item COMP (free, definately not recommended for signups)

=item PREPAY (special billing type: applies a credit (see FS::prepay_credit) and sets billing type to BILL)

=back

=item cvv_enabled

True if CVV features are available (1.5+ or 1.4.2 with CVV schema patch)

=item msgcat

Hash reference of message catalog values, to support error message customization.  Currently available keys are: passwords_dont_match, invalid_card, unknown_card_type, and not_a (as in "Not a Discover card").  Values are configured in the web interface under "View/Edit message catalog".

=item statedefault

Default state

=item countrydefault

Default country

=back

=item new_customer HASHREF

Creates a new customer.  Takes a hash reference as parameter with the
following keys:

=over 4

=item first - first name (required)

=item last - last name (required)

=item ss (not typically collected; mostly used for ACH transactions)

=item company

=item address1 (required)

=item address2

=item city (required)

=item county

=item state (required)

=item zip (required)

=item daytime - phone

=item night - phone

=item fax - phone

=item payby - CARD, DCRD, CHEK, DCHK, LECB, BILL, COMP or PREPAY (see L</signup_info> (required)

=item payinfo - Card number for CARD/DCRD, account_number@aba_number for CHEK/DCHK, prepaid "pin" for PREPAY, purchase order number for BILL

=item paycvv - Credit card CVV2 number (1.5+ or 1.4.2 with CVV schema patch)

=item paydate - Expiration date for CARD/DCRD

=item payname - Exact name on credit card for CARD/DCRD, bank name for CHEK/DCHK

=item invoicing_list - comma-separated list of email addresses for email invoices.  The special value 'POST' is used to designate postal invoicing (it may be specified alone or in addition to email addresses),

=item referral_custnum - referring customer number

=item pkgpart - pkgpart of initial package

=item username

=item _password

=item sec_phrase - security phrase

=item popnum - access number (index, not the literal number)

=item agentnum - agent number

=back

Returns a hash reference with the following keys:

=over 4

=item error Empty on success, or an error message on errors.  The special error '_decline' is returned for declined transactions; other error messages should be suitable for display to the user (and are customizable in under Sysadmin | View/Edit message catalog)

=back

=item regionselector HASHREF | LIST

Takes as input a hashref or list of key/value pairs with the following keys:

=over 4

=item selected_county

=item selected_state

=item selected_country

=item prefix - Specify a unique prefix string  if you intend to use the HTML output multiple time son one page.

=item onchange - Specify a javascript subroutine to call on changes

=item default_state

=item default_country

=item locales - An arrayref of hash references specifying regions.  Normally you can just pass the value of the I<cust_main_county> field returned by B<signup_info>.

=back

Returns a list consisting of three HTML fragments for county selection,
state selection and country selection, respectively.

=cut

#false laziness w/FS::cust_main_county (this is currently the "newest" version)
sub regionselector {
  my $param;
  if ( ref($_[0]) ) {
    $param = shift;
  } else {
    $param = { @_ };
  }
  $param->{'selected_country'} ||= $param->{'default_country'};
  $param->{'selected_state'} ||= $param->{'default_state'};

  my $prefix = exists($param->{'prefix'}) ? $param->{'prefix'} : '';

  my $countyflag = 0;

  my %cust_main_county;

#  unless ( @cust_main_county ) { #cache 
    #@cust_main_county = qsearch('cust_main_county', {} );
    #foreach my $c ( @cust_main_county ) {
    foreach my $c ( @{ $param->{'locales'} } ) {
      #$countyflag=1 if $c->county;
      $countyflag=1 if $c->{county};
      #push @{$cust_main_county{$c->country}{$c->state}}, $c->county;
      #$cust_main_county{$c->country}{$c->state}{$c->county} = 1;
      $cust_main_county{$c->{country}}{$c->{state}}{$c->{county}} = 1;
    }
#  }
  $countyflag=1 if $param->{selected_county};

  my $script_html = <<END;
    <SCRIPT>
    function opt(what,value,text) {
      var optionName = new Option(text, value, false, false);
      var length = what.length;
      what.options[length] = optionName;
    }
    function ${prefix}country_changed(what) {
      country = what.options[what.selectedIndex].text;
      for ( var i = what.form.${prefix}state.length; i >= 0; i-- )
          what.form.${prefix}state.options[i] = null;
END
      #what.form.${prefix}state.options[0] = new Option('', '', false, true);

  foreach my $country ( sort keys %cust_main_county ) {
    $script_html .= "\nif ( country == \"$country\" ) {\n";
    foreach my $state ( sort keys %{$cust_main_county{$country}} ) {
      my $text = $state || '(n/a)';
      $script_html .= qq!opt(what.form.${prefix}state, "$state", "$text");\n!;
    }
    $script_html .= "}\n";
  }

  $script_html .= <<END;
    }
    function ${prefix}state_changed(what) {
END

  if ( $countyflag ) {
    $script_html .= <<END;
      state = what.options[what.selectedIndex].text;
      country = what.form.${prefix}country.options[what.form.${prefix}country.selectedIndex].text;
      for ( var i = what.form.${prefix}county.length; i >= 0; i-- )
          what.form.${prefix}county.options[i] = null;
END

    foreach my $country ( sort keys %cust_main_county ) {
      $script_html .= "\nif ( country == \"$country\" ) {\n";
      foreach my $state ( sort keys %{$cust_main_county{$country}} ) {
        $script_html .= "\nif ( state == \"$state\" ) {\n";
          #foreach my $county ( sort @{$cust_main_county{$country}{$state}} ) {
          foreach my $county ( sort keys %{$cust_main_county{$country}{$state}} ) {
            my $text = $county || '(n/a)';
            $script_html .=
              qq!opt(what.form.${prefix}county, "$county", "$text");\n!;
          }
        $script_html .= "}\n";
      }
      $script_html .= "}\n";
    }
  }

  $script_html .= <<END;
    }
    </SCRIPT>
END

  my $county_html = $script_html;
  if ( $countyflag ) {
    $county_html .= qq!<SELECT NAME="${prefix}county" onChange="$param->{'onchange'}">!;
    $county_html .= '</SELECT>';
  } else {
    $county_html .=
      qq!<INPUT TYPE="hidden" NAME="${prefix}county" VALUE="$param->{'selected_county'}">!;
  }

  my $state_html = qq!<SELECT NAME="${prefix}state" !.
                   qq!onChange="${prefix}state_changed(this); $param->{'onchange'}">!;
  foreach my $state ( sort keys %{ $cust_main_county{$param->{'selected_country'}} } ) {
    my $text = $state || '(n/a)';
    my $selected = $state eq $param->{'selected_state'} ? 'SELECTED' : '';
    $state_html .= "\n<OPTION $selected VALUE=$state>$text</OPTION>"
  }
  $state_html .= '</SELECT>';

  $state_html .= '</SELECT>';

  my $country_html = qq!<SELECT NAME="${prefix}country" !.
                     qq!onChange="${prefix}country_changed(this); $param->{'onchange'}">!;
  my $countrydefault = $param->{default_country} || 'US';
  foreach my $country (
    sort { ($b eq $countrydefault) <=> ($a eq $countrydefault) or $a cmp $b }
      keys %cust_main_county
  ) {
    my $selected = $country eq $param->{'selected_country'} ? ' SELECTED' : '';
    $country_html .= "\n<OPTION$selected>$country</OPTION>"
  }
  $country_html .= '</SELECT>';

  ($county_html, $state_html, $country_html);

}

#=item expselect HASHREF | LIST
#
#Takes as input a hashref or list of key/value pairs with the following keys:
#
#=over 4
#
#=item prefix - Specify a unique prefix string  if you intend to use the HTML output multiple time son one page.
#
#=item date - current date, in yyyy-mm-dd or m-d-yyyy format
#
#=back

=item expselect PREFIX [ DATE ]

Takes as input a unique prefix string and the current expiration date, in
yyyy-mm-dd or m-d-yyyy format

Returns an HTML fragments for expiration date selection.

=cut

sub expselect {
  #my $param;
  #if ( ref($_[0]) ) {
  #  $param = shift;
  #} else {
  #  $param = { @_ };
  #my $prefix = $param->{'prefix'};
  #my $prefix = exists($param->{'prefix'}) ? $param->{'prefix'} : '';
  #my $date =   exists($param->{'date'})   ? $param->{'date'}   : '';
  my $prefix = shift;
  my $date = scalar(@_) ? shift : '';

  my( $m, $y ) = ( 0, 0 );
  if ( $date  =~ /^(\d{4})-(\d{2})-\d{2}$/ ) { #PostgreSQL date format
    ( $m, $y ) = ( $2, $1 );
  } elsif ( $date =~ /^(\d{1,2})-(\d{1,2}-)?(\d{4}$)/ ) {
    ( $m, $y ) = ( $1, $3 );
  }
  my $return = qq!<SELECT NAME="$prefix!. qq!_month" SIZE="1">!;
  for ( 1 .. 12 ) {
    $return .= "<OPTION";
    $return .= " SELECTED" if $_ == $m;
    $return .= ">$_";
  }
  $return .= qq!</SELECT>/<SELECT NAME="$prefix!. qq!_year" SIZE="1">!;
  my @t = localtime;
  my $thisYear = $t[5] + 1900;
  for ( ($thisYear > $y && $y > 0 ? $y : $thisYear) .. 2037 ) {
    $return .= "<OPTION";
    $return .= " SELECTED" if $_ == $y;
    $return .= ">$_";
  }
  $return .= "</SELECT>";

  $return;
}

=item popselector HASHREF | LIST

Takes as input a hashref or list of key/value pairs with the following keys:

=over 4

=item popnum

=item pops - An arrayref of hash references specifying access numbers.  Normally you can just pass the value of the I<svc_acct_pop> field returned by B<signup_info>.

=back

Returns an HTML fragment for access number selection.

=cut

#horrible false laziness with FS/FS/svc_acct_pop.pm::popselector
sub popselector {
  my $param;
  if ( ref($_[0]) ) {
    $param = shift;
  } else {
    $param = { @_ };
  }
  my $popnum = $param->{'popnum'};
  my $pops = $param->{'pops'};

  return '<INPUT TYPE="hidden" NAME="popnum" VALUE="">' unless @$pops;
  return $pops->[0]{city}. ', '. $pops->[0]{state}.
         ' ('. $pops->[0]{ac}. ')/'. $pops->[0]{exch}. '-'. $pops->[0]{loc}.
         '<INPUT TYPE="hidden" NAME="popnum" VALUE="'. $pops->[0]{popnum}. '">'
    if scalar(@$pops) == 1;

  my %pop = ();
  my %popnum2pop = ();
  foreach (@$pops) {
    push @{ $pop{ $_->{state} }->{ $_->{ac} } }, $_;
    $popnum2pop{$_->{popnum}} = $_;
  }

  my $text = <<END;
    <SCRIPT>
    function opt(what,href,text) {
      var optionName = new Option(text, href, false, false)
      var length = what.length;
      what.options[length] = optionName;
    }
END

  my $init_popstate = $param->{'init_popstate'};
  if ( $init_popstate ) {
    $text .= '<INPUT TYPE="hidden" NAME="init_popstate" VALUE="'.
             $init_popstate. '">';
  } else {
    $text .= <<END;
      function acstate_changed(what) {
        state = what.options[what.selectedIndex].text;
        what.form.popac.options.length = 0
        what.form.popac.options[0] = new Option("Area code", "-1", false, true);
END
  } 

  my @states = $init_popstate ? ( $init_popstate ) : keys %pop;
  foreach my $state ( sort { $a cmp $b } @states ) {
    $text .= "\nif ( state == \"$state\" ) {\n" unless $init_popstate;

    foreach my $ac ( sort { $a cmp $b } keys %{ $pop{$state} }) {
      $text .= "opt(what.form.popac, \"$ac\", \"$ac\");\n";
      if ($ac eq $param->{'popac'}) {
        $text .= "what.form.popac.options[what.form.popac.length-1].selected = true;\n";
      }
    }
    $text .= "}\n" unless $init_popstate;
  }
  $text .= "popac_changed(what.form.popac)}\n";

  $text .= <<END;
  function popac_changed(what) {
    ac = what.options[what.selectedIndex].text;
    what.form.popnum.options.length = 0;
    what.form.popnum.options[0] = new Option("City", "-1", false, true);

END

  foreach my $state ( @states ) {
    foreach my $popac ( keys %{ $pop{$state} } ) {
      $text .= "\nif ( ac == \"$popac\" ) {\n";

      foreach my $pop ( @{$pop{$state}->{$popac}}) {
        my $o_popnum = $pop->{popnum};
        my $poptext =  $pop->{city}. ', '. $pop->{state}.
                       ' ('. $pop->{ac}. ')/'. $pop->{exch}. '-'. $pop->{loc};

        $text .= "opt(what.form.popnum, \"$o_popnum\", \"$poptext\");\n";
        if ($popnum == $o_popnum) {
          $text .= "what.form.popnum.options[what.form.popnum.length-1].selected = true;\n";
        }
      }
      $text .= "}\n";
    }
  }


  $text .= "}\n</SCRIPT>\n";

  $text .=
    qq!<TABLE CELLPADDING="0"><TR><TD><SELECT NAME="acstate"! .
    qq!SIZE=1 onChange="acstate_changed(this)"><OPTION VALUE=-1>State!;
  $text .= "<OPTION" . ($_ eq $param->{'acstate'} ? " SELECTED" : "") .
           ">$_" foreach sort { $a cmp $b } @states;
  $text .= '</SELECT>'; #callback? return 3 html pieces?  #'</TD>';

  $text .=
    qq!<SELECT NAME="popac" SIZE=1 onChange="popac_changed(this)">!.
    qq!<OPTION>Area code</SELECT></TR><TR VALIGN="top">!;

  $text .= qq!<TR><TD><SELECT NAME="popnum" SIZE=1 STYLE="width: 20em"><OPTION>City!;


  #comment this block to disable initial list polulation
  my @initial_select = ();
  if ( scalar( @$pops ) > 100 ) {
    push @initial_select, $popnum2pop{$popnum} if $popnum2pop{$popnum};
  } else {
    @initial_select = @$pops;
  }
  foreach my $pop ( sort { $a->{state} cmp $b->{state} } @initial_select ) {
    $text .= qq!<OPTION VALUE="!. $pop->{popnum}. '"'.
             ( ( $popnum && $pop->{popnum} == $popnum ) ? ' SELECTED' : '' ). ">".
             $pop->{city}. ', '. $pop->{state}.
               ' ('. $pop->{ac}. ')/'. $pop->{exch}. '-'. $pop->{loc};
  }

  $text .= qq!</SELECT></TD></TR></TABLE>!;

  $text;

}

=back

=head1 RESELLER FUNCTIONS

Note: Resellers can also use the B<signup_info> and B<new_customer> functions
with their active session, and the B<customer_info> and B<order_pkg> functions
with their active session and an additonal I<custnum> parameter.

=over 4

=item agent_login

=item agent_info

=item agent_list_customers

=back

=head1 BUGS

=head1 SEE ALSO

L<freeside-selfservice-clientd>, L<freeside-selfservice-server>

=cut

1;

