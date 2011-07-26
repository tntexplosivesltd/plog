# See LICENCE for licence details
# Or go to http://files.entropy.net.nz/LICENCE

#!/usr/bin/perl -w
use CGI qw(:standard);
use strict;

my $start = 0;
my $per_page = 8;
my @files = glob("posts/*");

print header;

print "<html>\n";
print "<head>\n";
print "<title>Test Script</title>\n";
print "</head>\n";
print "<body>\n";
print "<h1>Test perl script</h1>\n";
print "<h2>Files:</h2>\n";
print "<ul>\n";
if (($start +$per_page) > @files)
{
  $per_page = @files - $start;
}
for (my $i = $start; $i < $per_page; $i++)
{
  print "<li>$files[$i]</li>\n";
}
print "</ul>\n";
print "</body>\n";
print "</html>\n";
