function fib(n::num) {
    if (n == 0) {
        return 0;
    } 
    
    if (n==1){
        return 1;
    }

    return fib (n-1) + fib (n-2);

}

var x = fib(6);
consolelog(x);
