// Nesting of functions and lexical scoping
var i = 1;

function print(k::num) {
    k = 1;
    function foo() {
        k = 8;
        consolelog(k);
    }

    i = 8;
    foo();
    consolelog(k);
}

print();
consolelog(i);
