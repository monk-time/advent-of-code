'use strict';
let input = document.querySelector('pre').textContent,
    parens2int = ch => ch === '(' ? 1 : ch === ')' ? -1 : 0;
console.log('Final floor:', [...input].reduce((acc, el) => acc + parens2int(el), 0));

// ES2015 promises tail call optimisation, so one day this code should run much more efficiently.
// But so far this recursion doesn't seem to overflow the call stack.
function basement(arr, i=0, sum=0) {
    if (sum === -1) {
        return i; // position is 1-based
    } else if (i >= arr.length) {
        return 0;
    } else {
        return basement(arr, i + 1, sum + parens2int(arr[i]));
    }
}

console.log('Entered basement at:', basement(input));
