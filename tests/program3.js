var x = true;
print x;

function temp() {
    var x = 1;
    function temp() {
        var x = 2;
        return x;
    }

    if ( true ) {
        print "1";
    }
}
temp();

print x;
