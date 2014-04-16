var i =1;

function print(k::num) {
    function foo() {
        k = 5;
    }

    foo();
    consolelog(k);
}

print();
