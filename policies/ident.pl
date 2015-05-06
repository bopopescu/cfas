#!/usr/bin/perl

if ($ARGV[1] > 0) {
    $num = $ARGV[1];
}
else {
    $num = 0;
}

if ($ARGV[0] ne "") {
    open (IDENT, $ARGV[0]) or die "Could not open file $ARGV[0]: $!";
    open (IDENT2, ">$ARGV[0].new") or die "Could not open file $ARGV[0].new: $!";
    while($line = <IDENT>) {
        if (substr($line, 0, 1) eq " ") {
            $line = substr($line, $num);
        }
        print IDENT2 $line;
    }
    close(IDENT);
    close(IDENT2);
}
else {
    print "Please, specify the filename\n";
}
