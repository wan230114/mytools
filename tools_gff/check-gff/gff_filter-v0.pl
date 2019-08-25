#! /usr/bin/perl -w
use strict;
############################################################
use Getopt::Long;
my $opts = {};
GetOptions($opts, 'in=s', 'out=s', 'err=s');
$opts->{out} or $opts->{out} = 'STDOUT';
$opts->{err} or $opts->{err} = 'STDERR';
############################################################
open(IN, $opts->{in});
my $out_fh;
if($opts->{out} eq 'STDOUT') {$out_fh = \*STDOUT;} else {open($out_fh, '>', $opts->{out});}
my $err_fh;
if($opts->{err} eq 'STDERR') {$err_fh = \*STDERR;} else {open($err_fh, '>', $opts->{err});}
############################################################
my %database;
my %id_index;
my %parent_index;
my %chr_list;    # chromosome list, not now.
my $count = 0;
while(my $eachline = <IN>)
    {
    $count ++;
    chomp($eachline);
    if($eachline =~ m/^\s*$/) {next;}    # skip empty line.
    if($eachline =~ m/^#/) {next;} #####{$database{$count} = $eachline; next;}    # store #comment and ##meta directly.
    my @item = split("\t", $eachline);
    if($#item != 8) {print $err_fh "ERROR: Column-number: $count\n"; next;}    # throw column-number-error line without store. may cause further error for losing an parent record, like gene.
#    unless(exists($chr_list{$item[0]})) {print $err_fh "ERROR: Chr-name: $count\n"; next;}    #### quoted out now, for the %chr_list is not in use now. # throw chr-name-error line without store. may cause further error for losing an parent record, like gene.
    unless($item[2] =~ m/gene|transcript|mrna|cds/i) {print $err_fh "Warning: useless record: $count\n"; next;}    # throw useless records which is not gene|transcript|mrna|cds.
    if($item[3] =~ m/\D/) {print $err_fh "ERROR: Column3 contains non-numeric character: $count \#\#\#$item[3]\#\#\#\n"; next;}    # throw column4-containing-\D-error line without store.
    if($item[4] =~ m/\D/) {print $err_fh "ERROR: Column4 contains non-numeric character: $count\n"; next;}    # throw column5-containing-\D-error line without store.
    if($item[6] =~ m/[^+-.]/) {print $err_fh "ERROR: Column6 contains illigal character: $count\n"; next;}    # throw column7-containing-[^+-.]-error line without store.
    if($item[7] =~ m/[^012.]/) {print $err_fh "ERROR: Column7 contains illigal character: $count\n"; next;}    # throw column8-containing-[^012.]-error line without store.
    if($item[2] =~ m/cds/i and $item[7] =~ m/[^012]/) {print $err_fh "ERROR: CDS-record contains no phase : $count\n"; next;}    # throw CDS-record-without-phase line without store.
    if($item[2] =~ m/gene/i)
        {
        if($item[8] =~ m/id\=/i and &is_id_repeating($eachline)) {&save_record($count, $eachline); next;}    # for a gene record, skip tag'ID' and tag'Parent' check and save directly.
        else {print $err_fh "ERROR: gene-record contains no ID or repeating_ID : $count\n"; next;}    # throw no-ID-gene_record without saving.
        }
    unless($item[8] =~ m/ID\=/i and $item[8] =~ m/parent\=/i) {print $err_fh "ERROR: Column8 contains no-enough-tags: $count\n"; next;}    # throw record-without-'ID' and 'Parent' line without store.
    if(&is_id_repeating($eachline))
        {
        &save_record($count, $eachline);
        }
    else
        {
        print $err_fh "ERROR: record contains repeating ID: $count\n";    #throw record contains repeating ID without saving.
        }
    }    # after this cycle is over, the proper gff_records are saved in %database{$count}.
close(IN);
############################################################
my @number = sort { $a <=> $b } keys(%database);
foreach my $i (@number)    # check boundary
    {
    unless(ref($database{$i})) {next;}
    if($database{$i}->{col2} =~ m/gene/i) {next;}    # gene record is the top-level record, no boundary error.
    my $current_id = $database{$i}->{id};
    my $parent_id = $database{$i}->{parent};
    my @current_range = ($database{$i}->{col3}, $database{$i}->{col4});
    my $parent_count;
    if(exists($id_index{$parent_id}))    # check if its parent exists
        {
        $parent_count = $id_index{$parent_id};
        }
    else
        {
        print $err_fh "ERROR: parent id error: $i\n";
        $database{$i}->{is_normal} = 0;
        next;
        }
    my @parent_range = ($database{$parent_count}->{col3}, $database{$parent_count}->{col4});
    unless($current_range[0] >= $parent_range[0] and $current_range[1] <= $parent_range[1])
        {
        print $err_fh "ERROR: boundary error: $i\n";
        $database{$i}->{is_normal} = 0;
        }
    else
        {
        $database{$i}->{is_normal} = 1;
        }
    }    # after this, all %database record EXCEPT GENE RECORD got a $database{$count}->{is_normal} value, as 1 is normal, 0 is not normal.

foreach my $j (@number)
    {
    unless(ref($database{$j})) {next;}
    unless($database{$j}->{col2} =~ m/gene/i) {next;}
    my @child_list = @{&get_child_list($j)};
    foreach my $k (@child_list)
        {
        if(!exists(${$database{$k}}->{is_normal}) or ${$database{$k}}->{is_normal} eq 1)
            {${$database{$k}}->{is_normal} = 1; $database{$j}->{is_normal} = 1; next;}
        else {$database{$j}->{is_normal} = 0; last;}
        }
    }

foreach my $ii (@number)
    {
    unless(ref($database{$ii})) {next;}
    if($database{$ii}->{is_print} eq 1) {next;}
    $database{$ii}->{is_print} = 1;
    my @child_list = @{&get_child_list($ii)};
    OUTTER:foreach my $jj (@child_list)
        {
        if(${$database{$jj}}->{is_normal} eq 0)
            {
            foreach my $kk (@child_list) {${$database{$jj}}->{is_print} = 0;}
            ${$database{$ii}}->{is_print} = 0;
            last OUTTER;
            }
        else {${$database{$jj}}->{is_print} = 1;}
        }
    }

foreach my $jj (@number)
    {
    my %temp = %{$database{$jj}};
    if($temp{is_print} eq 1)
        {print $out_fh "$temp{col0}\t$temp{col1}\t$temp{col2}\t$temp{col3}\t$temp{col4}\t$temp{col5}\t$temp{col6}\t$temp{col7}\t$temp{col8}\n";}
    }
#############################################
sub is_id_repeating
    {
    my $line = shift(@_);
    my @item = split("\t", $line);
    my @attribute = split(";", $item[8]);
    foreach my $i (@attribute)
        {if($i =~ m/id\=(.+)/i)
            {my $id = $1;
            if(exists($id_index{$id}))
                {
                return(0);
                }
            else
                {
                return(1);
                }
            }
        }
    }

sub save_record
    {
    my $cnt = shift(@_);
    my $line = shift(@_);
    my @item = split("\t", $line);
    $database{$cnt}->{col0} = $item[0];
    $database{$cnt}->{col1} = $item[1];
    $database{$cnt}->{col2} = $item[2];
    $database{$cnt}->{col3} = $item[3];
    $database{$cnt}->{col4} = $item[4];
    $database{$cnt}->{col5} = $item[5];
    $database{$cnt}->{col6} = $item[6];
    $database{$cnt}->{col7} = $item[7];
    $database{$cnt}->{col8} = $item[8];
    #my @attribute = split(";", $item[8]);
    if($database{$cnt}->{col8} =~ m/id\=([^;]+)/i) {$database{$cnt}->{id} = $1;}    # save ID like another column
    $id_index{$database{$cnt}->{id}} = $cnt;    # make index of 'id->count'
    if($database{$cnt}->{col8} =~ m/parent\=([^;]+)/i) 
        {
        $database{$cnt}->{parent} = $1;    # save parent like another column
        push(@{$parent_index{$database{$cnt}->{parent}}}, $cnt);    #make index of 'parent->counts of records with such parent'
        }
    }

sub get_child_list
    {
    my $parent = shift(@_);
    if(!exists($parent_index{$parent}))
        {my @temp = (); return(\@temp); }
    else
        {
        my @child = @{$parent_index{$parent}};
        my @store;
        foreach my $i (@child)
            {
            push(@store, $i, @{&get_child_list($i)});
            }
        return \@store;
        }
    }
##################################################


