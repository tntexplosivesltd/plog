#!/usr/bin/env perl

package plog_utils;
use warnings;
use strict;

# Convert hex "hash" to string
sub hex_to_string
{
  my $hex = $_[0];
  $hex =~ s/([A-F0-9][A-F0-9])/chr(hex($1))/eig;
  return $hex;
}

# Convert string to hex "hash"
sub string_to_hex
{
  my $string = $_[0];
  $string =~ s/(.)/sprintf("%x", ord($1))/eg;
  return $string;
}

# parse a config file
sub parse_config
{
  my $config_file = $_[0];
  my (%settings, @setting, $line);
  open(SETTINGS, "<$config_file") || die "Could not open $config_file: $!\n";
  while(<SETTINGS>)
  {
    chomp($line = $_);
    next if ($line =~ /^#/);
    @setting = split(/\s*=\s*/, $line, 2) if ($line =~ /=/);
    $settings{$setting[0]} = $setting[1];
  }
  close(SETTINGS);
  return %settings;
}

1;
