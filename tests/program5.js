var m = "srijan";
var str = "sri";

function print(str::string) {
    var k = str;
    consolelog(k);
} 

print(m);


function callFunction(p::callback){
    p = function temp () {
        var car = str;
        print(car);
    };
}

// callFunction(p);


