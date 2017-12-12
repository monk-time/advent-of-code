'use strict';

var timed = f => { console.time('main'); f(); console.timeEnd('main'); }; // eslint-disable-line
timed(() => {
    /* --- PARSING --- */
    // An area is stored as a list of element-independent pairs of floors
    //   indicating where the components are stored, where each pair is
    //   a microchip and its matching generator (in that order).
    // A unique hash of an area (4 floors only) consists of
    //   two bits for the elevator and four bits per each pair of floors.
    // Example: 0:1hm.lm:2hg:3lg:4  - area
    //          0, [[0, 1], [0, 2]] - internal model (elev, area)
    //          00   0001    0010   - a binary value of a hash (incl. the elevator)
    const re = /\b(\w+?)(?:-compatible)? (microchip|generator)/;
    const addFloor = (acc, floor, i) => {
        const items = floor.split(/ an? /g).slice(1).map(item => re.exec(item));
        for (let [, elem, type] of items) {
            acc[elem] = acc[elem] || [];
            acc[elem][type[0] === 'm' ? 0 : 1] = i; // pairs are always [chip, gen]
        }
        return acc;
    };
    const parseArea = arr => Object.values(arr.reduce(addFloor, {}));
    const sortByMG = area => [...area].sort(([m1, g1], [m2, g2]) => m1 - m2 || g1 - g2);
    const hash = (area, elev) => sortByMG(area) // 4 floors * 8 items per floor = 32 bits
        .reduce((h, [m, g]) => (h << 4) + (m << 2) + g, elev);
    // const hashBin = (area, elev) => hash(area, elev)
    //     .toString(2).padStart(area.length * 4 + 2, '0')
    //     .replace(/(^.{2}|.{4}(?!$))/g,"$1 "); // space-delimited elevator and pairs
    // const repr = (area, elev) => `${elev}:` + sortByMG(area).map(it => it.join('')).join(',');

    // --- COMBINATIONS ---
    const move = (i, d) => pair => pair.map((el, j) => j === i ? el + d : el);
    const [mUp, mDown, gUp, gDown] = [move(0, 1), move(0, -1), move(1, 1), move(1, -1)];
    const pairUp   = ([m, g]) => [m + 1, g + 1];
    const pairDown = ([m, g]) => [m - 1, g - 1];
    const replace = (area, pair, i) => [...area.slice(0, i), pair, ...area.slice(i + 1)];
    const safe = area => {
        const [nSingleM, nG] = [[0, 0, 0, 0], [0, 0, 0, 0]]; // amount per floor
        for (let [m, g] of area) {
            nG[g] += 1; // both connected and unconnected (all are dangerous)
            if (m !== g) {
                nSingleM[m] += 1;
            }
        }
        // a floor is safe if it has either no unconnected chips or no gens
        return nSingleM.every((n, i) => n === 0 || nG[i] === 0);
    };
    const combs = function* ([pairF, mF, gF], area, floor) {
        let connectedPairTaken = false;
        for (let i = 0; i < area.length; i++) {
            if (!area[i].includes(floor)) continue;
            if (!connectedPairTaken && area[i][0] === area[i][1]) {
                connectedPairTaken = true; // OPTMZ: doesn't matter which one to take
                yield replace(area, pairF(area[i]), i); // take a connected pair
            }
            const [mHere, gHere] = [area[i][0] === floor, area[i][1] === floor];
            for (let j = i + 1; j < area.length; j++) {
                if (!area[j].includes(floor)) continue;
                if (mHere && area[j][0] === floor) { // take all pairs of microchips
                    yield replace(replace(area, mF(area[i]), i), mF(area[j]), j);
                }
                if (gHere && area[j][1] === floor) { // take all pairs of generators
                    yield replace(replace(area, gF(area[i]), i), gF(area[j]), j);
                }
            }
            if (mHere) {
                yield replace(area, mF(area[i]), i); // take all microships
            }
            if (gHere) {
                yield replace(area, gF(area[i]), i); // take all generators
            }
        }
    };
    const emptyBelow = (area, floor) => area.every(([m, g]) => m >= floor && g >= floor);
    const safeMoves = function* (area, floor) {
        if (floor < 3) {
            yield* [...combs([pairUp,   mUp,   gUp  ], area, floor)].filter(safe)
                .map(areaNew => ({ area: areaNew, floor: floor + 1 }));
        }
        if (floor > 0 && !emptyBelow(area, floor)) { // OPTMZ
            yield* [...combs([pairDown, mDown, gDown], area, floor)].filter(safe)
                .map(areaNew => ({ area: areaNew, floor: floor - 1 }));
        }
    };

    // --- BREADTH-FIRST SEARCH ---
    let dist = {};
    const bfs = (area, floor) => {
        let h = hash(area, floor);
        dist[h] = 0;
        let queue = [[area, floor, h]];
        while (queue.length) {
            [[area, floor, h], ...queue] = queue; // dequeue
            if (floor === 3 && emptyBelow(area, 3)) {
                return dist[h];
            }
            for (let { area: areaNew, floor: floorNew } of safeMoves(area, floor)) {
                const hashNew = hash(areaNew, floorNew);
                if (dist[hashNew] === undefined) { // unvisited
                    dist[hashNew] = dist[h] + 1;
                    queue.push([areaNew, floorNew, hashNew]);
                }
            }
        }
    };

    const input = document.body.textContent.trim().split('\n');
    let area = parseArea(input);

    console.log('Shortest path length (part 1):', bfs(area, 0));
    console.log('Keys in cache:', Object.keys(dist).length);

    dist = {};
    area = [...area, [0, 0], [0, 0]];
    console.log('Shortest path length (part 2):', bfs(area, 0));
    console.log('Keys in cache:', Object.keys(dist).length);

    // TODO: BFS with the queue as a sparse array of dists; q[Object.keys(q)[0]] for dequeueing.
});
