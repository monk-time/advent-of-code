// 350 ms, generates all permutations of cities, small memory usage
// (updates min-max dist. on-the-fly instead of storing all distances in a 8!-length array)

'use strict';
// basic perm. generator with abstracted out storage function - reusable! :lol:
function permute(input, pusher = (acc, arr) => acc.push(arr.slice()), acc = []) {
    let used = [];
    function genPerm() {
        if (input.length === 0) {
            pusher(acc, used);
        }

        for (let i = 0; i < input.length; i++) {
            let [ch] = input.splice(i, 1);
            used.push(ch);
            genPerm();
            input.splice(i, 0, ch);
            used.pop();
        }
    }

    genPerm();
    return acc;
}

function addDist(dists, line) { // mutates dists
    let [a, b, dist] = line.split(/ to | = /);
    for (let [from, to] of [[a, b], [b, a]]) {
        dists[from] = dists[from] || {};
        dists[from][to] = +dist;
    }

    return dists;
}

function travel(dists, route) {
    let [prev, ...rest] = route;
    return rest.reduce(({ prev, sum }, next) =>
        ({ prev: next, sum: sum + dists[prev][next] }),
    { prev, sum: 0 }).sum;
}

function minmax(n, { min, max }) {
    min = min === undefined ? n : Math.min(n, min);
    max = max === undefined ? n : Math.max(n, max);
    return { min, max };
}

let input = document.body.textContent.trim().split('\n'),
    dists = input.reduce(addDist, {}),
    cities = Object.keys(dists),
    trackMinmax = (acc, r) => Object.assign(acc, minmax(travel(dists, r), acc)),
    lenArr = permute(cities, trackMinmax, {});
console.log(lenArr);
