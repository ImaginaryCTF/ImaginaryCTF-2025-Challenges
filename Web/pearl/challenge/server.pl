#!/usr/bin/perl

use strict;
use warnings;
use HTTP::Daemon;
use HTTP::Status;
use File::Spec;
use File::MimeInfo::Simple;
use File::Basename;
use CGI qw(escapeHTML);
use POSIX ":sys_wait_h";

$SIG{CHLD} = 'IGNORE';  # Prevent zombies

my $webroot = "./files";

my $d = HTTP::Daemon->new(LocalAddr => '0.0.0.0', LocalPort => 8080, Reuse => 1)
    || die "Failed to start server: $!";

print "Server running at: ", $d->url, "\n";

while (my $c = $d->accept) {
    my $pid = fork();
    if (!defined $pid) {
        warn "fork failed: $!";
        next;
    }
    if ($pid == 0) {
        # Child process handles this client
        while (my $r = $c->get_request) {
            if ($r->method eq 'GET') {
                my $path = CGI::unescape($r->uri->path);
                $path =~ s|^/||;
                $path ||= 'index.html';

                my $fullpath = File::Spec->catfile($webroot, $path);

                if ($fullpath =~ /\.\.|[,\`\)\(;&]|\|.*\|/) {
                    $c->send_error(RC_BAD_REQUEST, "Invalid path");
                    next;
                }

                if (-d $fullpath) {
                    opendir(my $dh, $fullpath) or do {
                        $c->send_error(RC_FORBIDDEN, "Cannot open directory.");
                        next;
                    };
                    my @files = readdir($dh);
                    closedir($dh);

                    my $html = "<html><body><h1>Index of /$path</h1><ul>";
                    foreach my $f (@files) {
                        next if $f =~ /^\./;
                        my $link = "$path/$f";
                        $link =~ s|//|/|g;
                        $html .= qq{<li><a href="/$link">} . escapeHTML($f) . "</a></li>";
                    }
                    $html .= "</ul></body></html>";

                    my $resp = HTTP::Response->new(RC_OK);
                    $resp->header("Content-Type" => "text/html");
                    $resp->content($html);
                    $c->send_response($resp);

                } else {
                    open(my $fh, $fullpath) or do {
                        $c->send_error(RC_INTERNAL_SERVER_ERROR, "Could not open file.");
                        next;
                    };
                    binmode $fh;
                    my $content = do { local $/; <$fh> };
                    close $fh;

                    my $mime = 'text/html';

                    my $resp = HTTP::Response->new(RC_OK);
                    $resp->header("Content-Type" => $mime);
                    $resp->content($content);
                    $c->send_response($resp);
                }
            } else {
                $c->send_error(RC_METHOD_NOT_ALLOWED);
            }
        }
        $c->close;
        exit(0);  # Child exits after finishing with this client
    } else {
        # Parent just goes back to accept loop
        $c->close;
    }
}
