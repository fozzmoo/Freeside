<!-- $Id: part_bill_event.cgi,v 1.3 2002-01-30 18:22:54 ivan Exp $ -->

<%

if ( $cgi->param('eventpart') && $cgi->param('eventpart') =~ /^(\d+)$/ ) {
  $cgi->param('eventpart', $1);
} else {
  $cgi->param('eventpart', '');
}

my ($query) = $cgi->keywords;
my $action = '';
my $part_bill_event = '';
if ( $cgi->param('error') ) {
  $part_bill_event = new FS::part_bill_event ( {
    map { $_, scalar($cgi->param($_)) } fields('part_bill_event')
  } );
}
if ( $query && $query =~ /^(\d+)$/ ) {
  $part_bill_event ||= qsearchs('part_bill_event',{'eventpart'=>$1});
} else {
  $part_bill_event ||= new FS::part_bill_event {};
}
$action ||= $part_bill_event->pkgpart ? 'Edit' : 'Add';
my $hashref = $part_bill_event->hashref;

print header("$action Invoice Event Definition", menubar(
  'Main Menu' => popurl(2),
  'View all invoice events' => popurl(2). 'browse/part_bill_event.cgi',
));

print qq!<FONT SIZE="+1" COLOR="#ff0000">Error: !, $cgi->param('error'),
      "</FONT>"
  if $cgi->param('error');

print '<FORM ACTION="', popurl(1), 'process/part_bill_event.cgi" METHOD=POST>'.
      '<INPUT TYPE="hidden" NAME="eventpart" VALUE="'.
      $part_bill_event->eventpart  .'">';
print "Invoice Event #", $hashref->{eventpart} ? $hashref->{eventpart} : "(NEW)";

print ntable("#cccccc",2), <<END;
<TR><TD ALIGN="right">Payby</TD><TD><SELECT NAME="payby">
END

for (qw(CARD BILL COMP)) {
  print qq!<OPTION VALUE="$_"!;
  if ($part_bill_event->payby eq $_) {
    print " SELECTED> $_</OPTION>";
  } else {
    print ">$_</OPTION>";
  }
}

my $days = $hashref->{seconds}/86400;

print <<END;
</SELECT></TD></TR>
<TR><TD ALIGN="right">Event</TD><TD><INPUT TYPE="text" NAME="event" VALUE="$hashref->{event}"></TD></TR>
<TR><TD ALIGN="right">After</TD><TD><INPUT TYPE="text" NAME="days" VALUE="$days"> days</TD></TR>
END

print '<TR><TD ALIGN="right">Disabled</TD><TD>';
print '<INPUT TYPE="checkbox" NAME="disabled" VALUE="Y"';
print ' CHECKED' if $hashref->{disabled} eq "Y";
print '>';
print '</TD></TR>';

print '<TR><TD ALIGN="right">Action</TD><TD>';

#print ntable();

#this is pretty kludgy right here.
tie my %events, 'Tie::IxHash',

  'fee' => {
    'name'   => 'Late fee',
    'code'   => '$cust_main->charge( %%%charge%%%, \'%%%reason%%%\' );',
    'html'   => 
      'Amount <INPUT TYPE="text" SIZE="7" NAME="charge" VALUE="%%%charge%%%">'.
      '<BR>Reason <INPUT TYPE="text" NAME="reason" VALUE="%%%reason%%%">',
    'weight' => 10,
  },
  'suspend' => {
    'name'   => 'Suspend',
    'code'   => '$cust_main->suspend();',
    'weight' => 10,
  },
  'cancel' => {
    'name'   => 'Cancel',
    'code'   => '$cust_main->cancel();',
    'weight' => 10,
  },

  'addpost' => {
    'name' => 'Add postal invoicing',
    'code' => '$cust_main->invoicing_list_addpost();',
    'pad'  => 20,
  },

  'send' => {
    'name' => 'Send invoice (email/print)',
    'code' => '',
    'weight' => 30
  },

  'bill' => {
    'name' => 'Generate invoices',
    'code' => '$cust_main->bill();',
    'weight'  => 40,
  },

  'apply' => {
    'name' => 'Apply unapplied payments and credits',
    'code' => '$cust_main->apply_payments; $cust_main->apply_credits;',
    'weight'  => 50,
  },

  'collect' => {
    'name' => 'Collect on invoices',
    'code' => '$cust_main->collect();',
    'weight'  => 60,
  },

;

foreach my $event ( keys %events ) {
  my %plandata = map { /^(\w+) (.*)$/; ($1, $2); }
                   split(/\n/, $part_bill_event->plandata);
  my $html = $events{$event}{html};
  while ( $html =~ /%%%(\w+)%%%/ ) {
    my $field = $1;
    $html =~ s/%%%$field%%%/$plandata{$field}/;
  }

  print ntable( "#cccccc", 2).
        qq!<TR><TD><INPUT TYPE="radio" NAME="plan_weight_eventcode" !;
  print "CHECKED " if $event eq $part_bill_event->plan;
  print qq!VALUE="!.  $event. ":". $events{$event}{weight}. ":".
        encode_entities($events{$event}{code}).
        qq!">$events{$event}{name}</TD>!;
  print '<TD>'. $html. '</TD>' if $html;
  print qq!</TR>!;
  print '</TABLE>';
}

#print '</TABLE>';

print <<END;
</TD></TR>
</TABLE>
END

print qq!<INPUT TYPE="submit" VALUE="!,
      $hashref->{eventpart} ? "Apply changes" : "Add invoice event",
      qq!">!;
%>

    </FORM>
  </BODY>
</HTML>

