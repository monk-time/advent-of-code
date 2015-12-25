'use strict';
function* selectSumN(arr, n) { // arr must be sorted
    let [stack, i, sum] = [[], 0, 0];
    do {
        let nextSum = sum + arr[i];
        if (nextSum < n && i < arr.length - 1) {
            stack.push(i++);
            sum = nextSum;
        } else {
            if (nextSum === n) {
                let seq = [...stack, i].map(ind => arr[ind]),
                    rest = arr.filter(el => !seq.includes(el));
                yield { seq, rest };
            }

            do {
                i = stack.pop();
                sum -= arr[i];
            } while (stack.length && i === arr.length - 1);

            i++;
        }
    } while (i < arr.length);
}

function* splitEqual(arr, parts) {
    arr.sort((a, b) => a - b);
    let onePart = arr.reduce((a, b) => a + b, 0) / parts;
    for (let { seq, rest } of selectSumN(arr, onePart)) {
        let secondGroup = selectSumN(rest, onePart);
        if (secondGroup.next().value) { // undefined if can't split the rest in two
            yield seq;
        }
    }
}

function minGroupQE(arr, parts) {
    let [minLength, minQE] = [Infinity, Infinity];
    for (let seq of splitEqual(arr, parts)) {
        if (seq.length < minLength) {
            minQE = seq.reduce((a, b) => a * b, 1);
            minLength = seq.length;
        } else if (seq.length === minLength) {
            minQE = Math.min(minQE, seq.reduce((a, b) => a * b, 1));
        }
    }

    return minQE;
}

let input = document.body.textContent.trim().split('\n').map(n => +n);

console.log(minGroupQE(input, 4));
// 70 sec for part 1, 25 sec for part 2
