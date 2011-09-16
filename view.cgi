#!/usr/bin/perl -w

# See LICENCE for licence details
# Or go to http://files.entropy.net.nz/LICENCE

use CGI qw(:standard start_ul);
use CGI::Carp qw(fatalsToBrowser);
use strict;

sub print_post
{
  my $line;
  my $title_found = 0;
  my $file = $_[0];
  open(POST_FILE, "<$file") || die "Could not open $file: $!\n";
  $line = <POST_FILE>;
  return if (!$line);

  chomp ($line);
  print $q->h2($line),"\n";
  while(<POST_FILE>)
  {
    chomp($line = $_);
    print "$line\n";
  }
}


my $start;
my $per_page;
my @files = glob("posts/*");
my $q = CGI->new;


# take parameters and assign defaults if non-exist
$start = $q->param("start");
$per_page = $q->param("per_page");
$start = 0 unless defined($start);
$per_page = 8 unless defined($per_page);
$start = abs($start);
$per_page = abs($per_page);

# print start of page
print $q->header,
      $q->start_html("Blog - entropy.net.nz"),
      $q->h1("Blog"),"\n",
      $q->h2("Posts"),"\n",
      $q->start_ul();

# validate parameters
$start = @files - 1 if ($start > @files);
$per_page = @files - $start if (($start + $per_page) > @files);
$per_page = 1 if ($per_page < 1);

# print out list of files
for (my $i = $start; $i < $start+$per_page; $i++)
{
  #print $q->li("$files[$i]"),"\n";
  print_post($files[$i]);
}

# print tail of HTML
print $q->end_ul(),"\n";
print "Start: $start, per_page: $per_page\n";
print $q->end_html();
