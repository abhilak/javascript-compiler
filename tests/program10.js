var m = function call(t::callback) {
    t();
};

m(function () {
    consolelog(1);
});
