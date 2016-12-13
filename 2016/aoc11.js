'use strict';

{
    /* --- PARSING --- */
    const re = /\b(\w+?)(?:-compatible)? (microchip|generator)/;
    const parseItem = s => (m => m && [m[1], m[2][0]] || [])(s.match(re));
    const parseFloor = s => s.split(/ an? /g).slice(1).map(parseItem);
    const not = type => type === 'm' ? 'g' : 'm';
    const byType = items => items.reduce(
        (acc, [el, t]) => ({ [t]: [...acc[t], el].sort(), [not(t)]: acc[not(t)] }),
        { m: [], g: [] }
    );
    const normArea = area => {
        let [countElem, map] = [0, new Map()];
        return area.map(({ g, m }) => {
            const [gNorm, mNorm] = [[], []];
            // connected gens -> unconnected gens -> connected chips -> unconnected chips
            const gSorted = [...g.filter(x => m.includes(x)), ...g.filter(x => !m.includes(x))];
            for (let gen of gSorted) {
                if (!map.has(gen)) {
                    map.set(gen, 'abcdefghijklmnopqrstuvwxyz'[countElem++]);
                }
                gNorm.push(map.get(gen));
            }
            const mSorted = [...m.filter(x => g.includes(x)), ...m.filter(x => !g.includes(x))];
            for (let chp of mSorted) {
                if (!map.has(chp)) {
                    map.set(chp, 'abcdefghijklmnopqrstuvwxyz'[countElem++]);
                }
                mNorm.push(map.get(chp));
            }
            return { g: gNorm, m: mNorm };
        });
    };
    const parseArea = arr => normArea(arr.map(parseFloor).map(byType));
    const prefix = ([type, arr]) => arr.map(el => el + type).join('.');
    const hashFloor = ({ g, m }) => [['g', g], ['m', m]].map(prefix).filter(s => s).join('.');
    const hashState = (area, at = 0) =>
        `${at}:${normArea(area).reduce((s, fl, i) => `${s}${i}${hashFloor(fl)}`, '')}`;
    // const parseFloorHash = s => s ? s.split('.').map(s2 => s2.split('')) : [];
    // const parseHash = s => s.split(/\d+/).slice(2).map(parseFloorHash).map(byType);

    /* --- COMBINATIONS --- */
    const exclAll = (arr, excl) => excl.reduce((a, el) => a.filter(x => x !== el), arr);
    const allCombs = ({ g, m }) => {
        const move = (gens, chps) => ({
            take: { g: gens, m: chps },
            rest: { g: exclAll(g, gens), m: exclAll(m, chps) }
        });
        const [pairs, singles] = [[], []];
        let pairTaken = false;
        for (let i = 0; i < g.length; i++) { // must cover full range
            if (!pairTaken && m.includes(g[i])) {
                pairTaken = true; // OPTMZD: only move the smallest pair
                pairs.push(move([g[i]], [g[i]])); // take a connected pair
            }
            for (let j = i + 1; j < g.length; j++) {
                if (g.length === 2 || (!m.includes(g[i]) && !m.includes(g[j]))) {
                    pairs.push(move([g[i], g[j]], [])); // take two unconnected gens
                }
            }
        }
        for (let i = 0; i < m.length; i++) { // must cover full range
            for (let j = i + 1; j < m.length; j++) {
                pairs.push(move([], [m[i], m[j]])); // take two unconnected microchips
            }
        }
        if (g.length === 1) { // take a sole gen
            singles.push(move([g[0]], []));
        } else { // take only unconnected gens one by one
            singles.push(...g.filter(gen => !m.includes(gen)).map(gen => move([gen], [])));
        }
        // take all microchips ony by one (safe: either no gens or all chips are connected)
        singles.push(...m.map(chp => move([], [chp])));

        return { pairs, singles };
    };

    // --- FILTER ITEM COMBINATIONS SO THAT THE MOVE IS SAFE --- //
    // 'take' key is replaced by 'dest' after merging with a destination floor
    const safe = ({ g, m }) => g.length === 0 || m.every(el => g.includes(el));
    const merge = fl => ({ take, rest }) =>
        ({ rest, dest: { g: [...fl.g, ...take.g].sort(), m: [...fl.m, ...take.m].sort() } });
    const emptyBelow = (area, floor) =>
        area.slice(0, floor).every(({ g, m }) => g.length + m.length === 0);
    const combineMovers = arr => (({ g, m }) => ({ g: new Set(g), m: new Set(m) }))(arr.reduce(
        ({ g: gC, m: mC }, { take: { g, m } }) => ({ g: [...gC, ...g], m: [...mC, ...m] }),
        { g: [], m: [] }
    ));
    const moverNotIn = uniq => ({ take: { g, m } }) =>
        g.every(el => !uniq.g.has(el)) && m.every(el => !uniq.m.has(el));
    // OPTMZD: don't take one up if can take two with it, and vice versa down
    const preferRight = (moversL, moversR) => moversL.filter(moverNotIn(combineMovers(moversR)));
    const safeMoves = function* (area, floor) {
        const makeMove = (combs, toFloor) =>
            combs.map(merge(area[toFloor])).filter(({ dest }) => safe(dest));
        const { pairs, singles } = allCombs(area[floor]);
        if (floor < 3) { // go up
            const pairsUp = makeMove(pairs, floor + 1);
            const singlesUp = makeMove(pairsUp.length ? preferRight(singles, pairs) : singles, floor + 1);
            for (let { rest, dest } of [...pairsUp, ...singlesUp]) {
                const newArea = [...area.slice(0, floor), rest, dest, ...area.slice(floor + 2)];
                yield { area: newArea, floor: floor + 1 };
            }
        }
        if (floor > 0 && !emptyBelow(area, floor)) { // go down (OPTMZD: only if there are items below)
            // OPTMZD: doesn't matter which one item to take down
            let [singlesDown, gotOneChp, gotOneGen] = [[], false, false];
            for (let { take, rest } of singles) {
                // only one of m and d is not empty
                if (take.m.length && !gotOneChp) {
                    let moved = merge(area[floor - 1])({ take, rest });
                    if (safe(moved.dest)) {
                        singlesDown.push(moved);
                        gotOneChp = true;
                    }
                }
                if (take.g.length && !gotOneGen) {
                    let moved = merge(area[floor - 1])({ take, rest });
                    if (safe(moved.dest)) {
                        singlesDown.push(moved);
                        gotOneGen = true;
                    }
                }
            }
            const pairsDown = makeMove(singlesDown.length ? preferRight(pairs, singles) : pairs, floor - 1);
            for (let { rest, dest } of [...singlesDown, ...pairsDown]) {
                const newArea = [...area.slice(0, floor - 1), dest, rest, ...area.slice(floor + 1)];
                yield { area: newArea, floor: floor - 1 };
            }
        }
    };

    /* --- BREADTH-FIRST SEARCH --- */
    let dist = {};
    const bfs = (area, floor) => {
        let hash = hashState(area, floor);
        dist[hash] = 0;
        let queue = [[area, floor, hash]];
        while (queue.length) {
            [[area, floor, hash], ...queue] = queue; // dequeue
            if (floor === 3 && emptyBelow(area, 3)) {
                return dist[hash];
            }
            for (let { area: areaNew, floor: floorNew } of safeMoves(area, floor)) {
                const hashNew = hashState(areaNew, floorNew);
                if (dist[hashNew] === undefined) { // unvisited
                    dist[hashNew] = dist[hash] + 1;
                    queue.push([areaNew, floorNew, hashNew]);
                }
            }
        }
    };

    const input = document.body.textContent.trim().split('\n');
    const area = parseArea(input);
    const timed = f => (...args) => { console.time('main'); f(...args); console.timeEnd('main'); };
    timed(() => console.log('Shortest path length (part 1):', bfs(area, 0)))();
    console.log('Keys in cache:', Object.keys(dist).length);

    const addPair = ({ g, m }, el) => ({ g: [...g, el], m: [...m, el] });
    area[0] = addPair(area[0], 'elerium');
    area[0] = addPair(area[0], 'dilithium');
    dist = {};
    timed(() => console.log('Shortest path length (part 2):', bfs(area, 0)))();
    console.log('Keys in cache:', Object.keys(dist).length);
    
    // TODO: re-do using a hash of [curFloor, [pairs]], where each pair consists of [chp, rtg]
    // TODO: BFS with the queue as a sparse array of dists; q[Object.keys(q)[0]] for dequeueing.
}
