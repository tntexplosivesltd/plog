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

sub get_include
{
  my $output;
  my $file = $_[0];
  open(INCLUDE, "<$ENV{'DOCUMENT_ROOT'}$file") || die "Could not open include file $file: $!\n";
  while(<INCLUDE>)
  {
    $output .= $_;
  }
  close(INCLUDE);
  return $output;
}

sub get_post
{
  my ($file, $q, %config) = @_;
  my ($body, $formatted_date, $formatted_time, $line, $post, @temp_body, $terminator, @time, $title);
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

  open(POST_TEMPLATE, "<$config{'post_template'}") || die "Could not open post template: $!\n";
  while (<POST_TEMPLATE>)
  {
    $line = $_;
    $line =~ s/!TITLE!/$title/g;
    $line =~ s/!DATE!/$formatted_date/g;
    $line =~ s/!TIME!/$formatted_time/g;
    $line =~ s/!BODY!/$body/g;
    $post .= $line;
  }
  close(POST_TEMPLATE);
  return $post;
}


my (@files, @includes, $nav_links, $next_page_start, $per_page, $post, $posts, $prev_page_start, $start, $supplied_per_page,);
my $q = CGI->new;
my %config = plog_utils::parse_config("config/view.conf");
my @include_files = split(/\s*,\s/, $config{'includes'});
for my $include(@include_files)
{
  push(@includes, get_include($include));
}

# take parameters and assign defaults if non-exist
$start = $q->param("start");
$per_page = $q->param("per_page");
$supplied_per_page = $per_page;
$post = $q->param("post");
$start = 0 unless ($start > 0);
$per_page = $config{'posts_per_page'} unless defined($per_page);
$per_page = abs($per_page);

if ($post)
{
  @files = "posts/$post";
  if (-e $files[0])
  {
    open(TITLE, "<$files[0]") || die "Can not open post $files[0]: $!\n";
    $config{'post_title'} = <TITLE> if ($config{'override'} eq "no");
    close(TITLE);
  }
}
else
{
  @files = reverse(glob("posts/*"));
}

# validate parameters
$start = @files - 1 if ($start > @files);
if (($start + $per_page) >= @files)
{
  $per_page = @files - $start;
}
$next_page_start = $start + $per_page;
$prev_page_start = $start - $supplied_per_page;
$prev_page_start = 0 if ($prev_page_start < 0);

for (my $i = $start; $i < $start+$per_page; $i++)
{
  $posts .= get_post($files[$i], $q, %config);
}

# Link to next page of posts
if ($start > 0)
{
  $nav_links .= $q->a({href=>"view.cgi?start=$prev_page_start&per_page=$supplied_per_page"}, "<- Previous"), "    "; 
}
# Link to previous posts
if ($next_page_start < @files)
{
  $nav_links .= $q->a({href=>"view.cgi?start=$next_page_start&per_page=$supplied_per_page"}, "Next ->");
}

print $q->header;
open(PAGE_TEMPLATE, "<$config{'page_template'}") || die "Could not open page template: $!\n";
while(<PAGE_TEMPLATE>)
{
  my $line = $_;
  $line =~ s/!POST_TITLE!/$config{'post_title'}/g;
  $line =~ s/!INCLUDE_(\d+)!/$includes[$1-1]/g;
  $line =~ s/!BLOG_TITLE!/$config{'blog_title'}/g;
  $line =~ s/!POSTS!/$posts/g;
  $line =~ s/!NAV_LINKS!/$nav_links/g;
  print $line;
}
close(PAGE_TEMPLATE);
