var m = function (t::bool) {
    if ( t ) {
        return 1;
    } else {
        return 2;
    }
};

function z(y::num, t::callback) {
    var k = y>2 && 1 < 2;
    m(true);
    t();
}
