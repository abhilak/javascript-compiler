var i =1;

function print(k::num) {
    k = 1;
    function foo() {
        k = 10;
        consolelog(k);
    }

    foo();
    consolelog(k);
}

print();
consolelog(i);
