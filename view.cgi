#!/usr/bin/perl -w

# See LICENCE for licence details
# Or go to http://files.entropy.net.nz/LICENCE

use CGI qw(:standard start_ul);
use strict;

my $start = 0;
my $per_page = 8;
my @files = glob("posts/*");
my $q = CGI->new;

print $q->header,
      $q->start_html("Blog - entropy.net.nz"),
      $q->h1("Test perl script"),"\n",
      $q->h2("Files:"),"\n",
      $q->start_ul();
if (($start +$per_page) > @files)
{
  $per_page = @files - $start;
}
for (my $i = $start; $i < $per_page; $i++)
{
  print $q->li("$files[$i]"),"\n";
}
print $q->end_ul();
print $q->end_html();
