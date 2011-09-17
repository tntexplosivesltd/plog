#!/usr/bin/env perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Date::Format;
use plog_utils;
use warnings;
use strict;


my ($title, $body, $error_css, $sep, %config);
my $q = CGI->new();
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime();

%config = plog_utils::parse_config();
$sep = "-";
$title = $q->param("title");
$body = $q->param("body");
if ($title || $body)
{
  my $name = plog_utils::string_to_hex($sec.$sep.$min.$sep.$hour.$sep.$mday.$sep.$mon.$sep.$year.$sep.$wday.$sep.$yday.$sep.$isdst);
  open(OUTPUT, ">posts/$name") || die "Could not open post output file: $!\n";
  print OUTPUT "$title\n";
  print OUTPUT $body;
  close(OUTPUT);
}
else
{
  print $q->header,
        $q->start_html(-title=>$config{'error_title'}),
        $q->p("Both title and body need to be filled in. Press back and try again"),
        $q->end_html(), "\n";
}
