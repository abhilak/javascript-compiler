
// Multiple loops
// Pattern

var i = 0;
var j = 0;

while ( i < 10 ) {
    j = 0;
    while( j < i ) {
        consolelog(j);
        j = j + 1;
    }
    consolelog("\n");
    i = i + 1;
}
