// https://adventofcode.com/2015/day/24

'use strict';

{
    const selectSumN = function* (arr, n) {
        arr = [...arr].sort((a, b) => a - b);
        const stack = [];
        let [i, sum] = [0, 0];
        while (i < arr.length) {
            const nextSum = sum + arr[i];
            if (nextSum < n && i < arr.length - 1) {
                stack.push(i++);
                sum = nextSum;
                continue;
            }

            if (nextSum === n) {
                const seq = [...stack, i].map(ind => arr[ind]);
                const rest = arr.filter(el => !seq.includes(el));
                yield { seq, rest };
            }

            do {
                i = stack.pop();
                sum -= arr[i];
            } while (stack.length && i === arr.length - 1);

            i++;
        }
    };

    const splitEqual = function* (arr, parts) {
        const onePart = arr.reduce((a, b) => a + b) / parts;
        for (const { seq, rest } of selectSumN(arr, onePart)) {
            const secondGroup = selectSumN(rest, onePart);
            if (secondGroup.next().value) { // undefined if can't split the rest in two
                yield seq;
            }
        }
    };

    const mul = arr => arr.reduce((a, b) => a * b);
    const minGroupQE = (arr, groups) => {
        let [minLength, minQE] = [Infinity, Infinity];
        for (const seq of splitEqual(arr, groups)) {
            if (seq.length < minLength) {
                minQE = mul(seq);
                minLength = seq.length;
            } else if (seq.length === minLength) {
                minQE = Math.min(minQE, mul(seq));
            }
        }

        return minQE;
    };

    const input = document.body.textContent.trim().split('\n').map(Number);
    console.log([3, 4].map(groups => minGroupQE(input, groups))); // 44 sec
}
