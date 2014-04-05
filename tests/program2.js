void(1);

function void(t::num) {
    t();
}

void(function () {
    var z = 1;
});
