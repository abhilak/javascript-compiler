var m = "srijan";
var str = "sri";

function print(str::string) {
    var k = str;
    consolelog(k);
} 

var p = print(m);


function callFunction(p::callback){
    p = function () {
        var car = str;
        print(car);
    };
}

callFunction(print);


