// multiple function calls
function temp () {
    function fib(n::num) {
        if (n == 0) {
            return 0;
        } else {
            return 2;
        }
    }

    var x = fib(3);
    console.log(x);
}

temp();
