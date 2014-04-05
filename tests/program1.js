function void() {
    var i = 0;
    while ( true ) {
        i = i + 1;
        if ( true ) {
            break;
        } else {
            continue;
        }
    }

    x(1);

    function x(y::num) {
        var k = y>2 && 1 < 2;
    }

    return 9;
}
