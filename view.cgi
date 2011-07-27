#!/usr/bin/perl -w

# See LICENCE for licence details
# Or go to http://files.entropy.net.nz/LICENCE

use CGI qw(:standard start_ul);
use strict;

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
      $q->h1("Test perl script"),"\n",
      $q->h2("Files:"),"\n",
      $q->start_ul();

# validate parameters
if ($start > @files)
{
  $start = @files - 1;
}
if (($start + $per_page) > @files)
{
  $per_page = @files - $start;
}

# print out list of files
for (my $i = $start; $i < $start+$per_page; $i++)
{
  print $q->li("$files[$i]"),"\n";
}

# print tail of HTML
print $q->end_ul();
print "Start: $start, per_page: $per_page\n";
print $q->end_html();
