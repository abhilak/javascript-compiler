var x = false;
var m = function(t::bool, x::callback) {
    x = true;
    return 1;

};
var y = m(x);
consolelog(y);
