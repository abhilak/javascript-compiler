// Anonymous functions and callbacks as parameters

var m = function call(t::callback) {
    t();
};

m(function () {
    consolelog(1);
});
