#!/usr/bin/env perl

# See LICENCE for licence details
# Or go to http://files.entropy.net.nz/LICENCE

use CGI qw(:standard start_ul);
use CGI::Carp qw(fatalsToBrowser);
use Date::Format;
use File::Basename;
use plog_utils;
use warnings;
use strict;

sub print_post
{
  my ($file, $q, %config) = @_;
  my ($body, $formatted_date, $formatted_time, $line, @temp_body, $terminator, @time, $title);
  my $title_found = 0;

  my $timedate = basename($file);
  #my $timedate = $file;
  ($time[5],$time[4],$time[3],$time[2],$time[1],$time[0],$time[6],$time[7],$time[8]) = split(/-/, $timedate);
  $formatted_time = strftime($config{'time_format'}, @time, $config{'timezone'});
  $formatted_date = strftime($config{'date_format'}, @time, $config{'timezone'});
  return if (!(-e $file) || (-z $file));
  open(POST_FILE, "<$file") || die "Could not open $file: $!\n";

  # Read post file and get title in one variable and body in another
  chomp($title = <POST_FILE>);
  $terminator = $/;
  @temp_body = <POST_FILE>;
  $body = join $terminator, @temp_body;
  close(POST_FILE);

  open(POST_TEMPLATE, "<$config{'template'}") || die "Could not open post template: $!\n";
  while (<POST_TEMPLATE>)
  {
    $line = $_;
    $line =~ s/!TITLE!/$title/g;
    $line =~ s/!DATE!/$formatted_date/g;
    $line =~ s/!TIME!/$formatted_time/g;
    $line =~ s/!BODY!/$body/g;
    print $line;
  }
  close(POST_TEMPLATE);
}


my (@files, $next, $per_page, $post, $start);;
my $q = CGI->new;
my %config = plog_utils::parse_config("config/view.conf");

# take parameters and assign defaults if non-exist
$start = $q->param("start");
$per_page = $q->param("per_page");
$post = $q->param("post");
$start = 0 unless defined($start);
$per_page = 8 unless defined($per_page);
$start = abs($start);
$per_page = abs($per_page);

if ($post)
{
  @files = "posts/$post";
  if (-e $files[0])
  {
    open(TITLE, "<$files[0]") || die "Can not open post $files[0]: $!\n";
    $config{'post_title'} = <TITLE> if ($config{'override'} eq "no");
    close (TITLE);
  }
}
else
{
  @files = reverse(glob("posts/*"));
}

# validate parameters
$start = @files - 1 if ($start > @files);
if (($start + $per_page) > @files)
{
  $per_page = @files - $start;
  $next = $start + $per_page;
}
$per_page = 1 if ($per_page < 1);


# print start of page
print $q->header,
      $q->start_html("$config{'post_title'}"),
      $q->h1("$config{'blog_title'}"),"\n";

# print out blog posts
for (my $i = $start; $i < $start+$per_page; $i++)
{
    print_post($files[$i], $q, %config);
}

# print tail of HTML
print $q->end_html();
