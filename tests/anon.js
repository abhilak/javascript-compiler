// Anonymous functions and callbacks as parameters

var m = function (t::callback) {
    t();
};

m(function () {
    consolelog(1);
});
