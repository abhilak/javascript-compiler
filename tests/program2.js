void(1);

function void(t::callback) {
    return 0;
}

void(function () {
    var z = 1;
});
