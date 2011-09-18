#!/usr/bin/env perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use plog_utils;
use warnings;
use strict;


my ($title, $body, $error_css, %config);
my $q = CGI->new();
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year += 1900;
$mon = sprintf("%02d", ($mon + 1));
$mday = sprintf("%02d", $mday);
$hour = sprintf("%02d", $hour);
$min = sprintf("%02d", $min);
$sec = sprintf("%02d", $sec);


%config = plog_utils::parse_config("../config/add.conf");
$title = $q->param("title");
$body = $q->param("body");
if ($title && $body)
{
  my $name = $year."-".$mon."-".$mday."-".$hour."-".$min."-".$sec."-".$wday."-".$yday."-".$isdst;
  open(OUTPUT, ">../posts/$name") || die "Could not open post output file: $!\n";
  print OUTPUT "$title\n";
  print OUTPUT $body;
  close(OUTPUT);
  # Go to post
  print $q->redirect("../view.cgi?post=".$name);
}
else
{
  print $q->header,
        $q->start_html(-title=>$config{'error_title'}),
        $q->p("Both title and body need to be filled in. Press back and try again"),
        $q->end_html(), "\n";
}
