package FS::part_export::hal_event_queue;

use strict;
use vars qw(%options %info);
use Tie::IxHash;
use base qw(FS::part_export);

use FS::UID qw/dbh/;
use FS::Record qw/qsearchs/;

use FS::event_queue;

tie my %options, 'Tie::IxHash',
    target      =>  {
        label   =>  "Target label (e.g. 'HP' for Hosting Platform)",
        default =>  'HP',
    },
;

%info = (
    'svc'       =>  'svc_external',
    'desc'      =>  'Export for HAL and other hosting platform service management',
    'options'   =>  \%options,
    'nodomain'  =>  'Y',
    'notes'     =>  <<'END'
Notes about this HAL event queue export.
END
);

sub rebless { shift; }

sub _export_insert {
    my ($self, $svc) = (shift, shift);

    my $target = $self->option('target');
    return new_event_queue_record($svc, 'insert', $target);
}

sub _export_delete {
    my ($self, $svc) = (shift, shift);

    my $target = $self->option('target');
    return new_event_queue_record($svc, 'delete', $target);
}

sub _export_replace {
    my ($self, $svc) = (shift, shift);

    my $target = $self->option('target');
    return new_event_queue_record($svc, 'replace', $target);
}

sub _export_suspend {
    my ($self, $svc) = (shift, shift);

    my $target = $self->option('target');
    return new_event_queue_record($svc, 'suspend', $target);
}

sub _export_unsuspend {
    my ($self, $svc) = (shift, shift);

    my $target = $self->option('target');
    return new_event_queue_record($svc, 'unsuspend', $target);
}

sub new_event_queue_record {
    my $svc = shift;
    my $action = shift;
    my $target = shift;

    my $eq_action = qsearchs('event_queue_action', { name => $action });
    my $eq_target = qsearchs('event_queue_target', { name => $target });

    my $event_queue = FS::event_queue->new({
        pkgnum      =>  $svc->cust_svc->cust_pkg->pkgnum,
        svcnum      =>  $svc->cust_svc->svcnum,
        eqaction    =>  $action->eqaction,
        eqtarget    =>  $target->eqtarget,
        agentnum    =>  $svc->cust_svc->cust_pkg->cust_main->agentnum,
    });
    my $error = $event_queue->insert;

    return $error if $error;

    my $eqs_status = qsearchs('event_queue_status', { name => 'queued' });
    my $event_queue_state = FS::event_queue_status->new({
        eqstatus    =>  $eqs_status->eqstatus,
        eqnum       =>  $event_queue->eqnum,
        date_set    =>  time,
    });
    $error = $event_queue_state->insert;

    return $error if $error;
    return '';
}

1;
