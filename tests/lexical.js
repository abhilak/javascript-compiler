// Nesting of functions and lexical scoping
var i = 1;

function print(k::num) {
    k = 1;
    function foo() {
        var k = 8;
        console.log(k);
    }

    i = 8;
    foo();
    console.log(k);
}

print();
console.log(i);
