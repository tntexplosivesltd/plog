#!/usr/bin/env perl

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use warnings;
use strict;

sub hex_to_string
{
  my $hex = $_[0];
  $hex =~ s/([A-F0-9][A-F0-9])/chr(hex($1))/eig;
  return $hex;
}

sub string_to_hex
{
  my $string = $_[0];
  $string =~ s/(.)/sprintf("%x", ord($1))/eg;
  return $string;
}

sub parse_config()
{
  my (%settings, @setting, $line);
  open(SETTINGS, "add.conf") || die "Could not open add config: $!\n";
  while(<SETTINGS>)
  {
    chomp($line = $_);
    @setting = split(/\s*=/,$line) if ($line =~ /=/);
    $settings{$setting[0]} = $setting[1];
  }
  close(SETTINGS);
  $settings{'error_title'} = "Error Occurred." if (!(exists $settings{'error_title'}));
  return %settings;
}

my ($title, $body, $error_css, %config);
my $q = CGI->new();
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();

%config = parse_config();
$title = $q->param("title");
$body = $q->param("body");
if ($title || $body)
{
  # Replace <,> with HTML codes to prevent naughtiness
  $title =~ s/</&lt;/g;
  $title =~ s/>/&gt;/g;
  $body =~ s/</&lt;/g;
  $body =~ s/>/&gt;/g;

}
else
{
  print $q->header,
        $q->start_html(-title=>$config{'error_title'}),
        $q->p("Both title and body need to be filled in. Press back and try again"),
        $q->end_html();
}

my $sep = "-";
my $time = string_to_hex($sec.$sep.$min.$sep.$hour.$sep.$mday.$sep.$mon.$sep.$year.$sep.$wday.$sep.$yday.$sep.$isdst);
my $reverse = hex_to_string($time);
print "$time\n$reverse\n";
