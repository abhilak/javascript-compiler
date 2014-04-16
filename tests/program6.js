// Function to display callbacks
function call(t::callback) {
    t();
}

// Anonymous functions
call(function() {
    consolelog(1);
    consolelog("true");
});

