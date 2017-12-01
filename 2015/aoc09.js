// 500 ms, generates all permutations of cities, small memory usage
// (updates min-max dist. on-the-fly instead of storing all distances in a 8!-length array)

'use strict';

{
    const permute = function* (arr, used = []) {
        if (arr.length === 0) yield [...used];
        for (let i = 0; i < arr.length; i++) {
            const [el] = arr.splice(i, 1);
            used.push(el);
            yield* permute(arr, used);
            arr.splice(i, 0, el);
            used.pop();
        }
    };

    const addDist = (dists, [a, b, n]) =>
        ({ ...dists, [a]: { ...dists[a], [b]: +n }, [b]: { ...dists[b], [a]: +n } });
    const travel = (dists, [prev0, ...rest]) => rest.reduce(
        ({ prev, sum }, next) => ({ prev: next, sum: sum + dists[prev][next] }),
        { prev: prev0, sum: 0 },
    ).sum;
    const updateMinMax = (n, [min = n, max = n]) => [Math.min(min, n), Math.max(max, n)];

    const input = document.body.textContent.trim().split('\n');
    const dists = input.map(s => s.split(/ to | = /)).reduce(addDist, {});

    let minmax = [];
    for (const route of permute(Object.keys(dists))) {
        minmax = updateMinMax(travel(dists, route), minmax);
    }

    console.log(minmax);
}
