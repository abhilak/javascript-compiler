
// Multiple function calls

var m = function (n::num) {
    consolelog(n);
};

var k = function () {
    m(1);
};

k();
