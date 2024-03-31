// https://adventofcode.com/2015/day/9

// 180 ms, generates all permutations of cities, small memory usage
// (updates min-max dist. on-the-fly instead of storing all distances in a 8!-length array)

'use strict';

{
    const extend = ([min, max], n) => [Math.min(min, n), Math.max(max, n)];
    const minmaxPerm = (arr, f, minmax = [Infinity, 0], used = []) => {
        if (arr.length === 0) return extend(minmax, f([...used]));
        for (let i = 0; i < arr.length; i++) {
            const [el] = arr.splice(i, 1);
            used.push(el);
            minmax = minmaxPerm(arr, f, minmax, used);
            arr.splice(i, 0, el);
            used.pop();
        }

        return minmax;
    };

    const input = document.body.textContent.trim().split('\n');
    const addDist = (o, [a, b, n]) =>
        ({ ...o, [a]: { ...o[a], [b]: +n }, [b]: { ...o[b], [a]: +n } });
    const dists = input.map(s => s.split(/ to | = /)).reduce(addDist, {});
    const travel = ([prev0, ...rest]) => rest.reduce(
        ({ prev, sum }, next) => ({ prev: next, sum: sum + dists[prev][next] }),
        { prev: prev0, sum: 0 },
    ).sum;

    console.log(minmaxPerm(Object.keys(dists), travel));
}
