var i =1;

function print(k::num) {
    k = 1;
    function foo() {
        k = 10;
    }

    foo();
    consolelog(k);
}

print();
consolelog(i);
