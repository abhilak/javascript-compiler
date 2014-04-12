function x(t::callback) {
    var i = 1;

    while ( i < 10 ) {
        i = i + 1;
        if ( i > 5) {
            break;
        } else {
            t(i);
            continue;
        }
    }
}

function printer(n::num) {
    var name = "srijan";
    consolelog(n);
    return 1;
}

x = printer(1);
