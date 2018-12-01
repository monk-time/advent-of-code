'use strict';

{
    const canConnect = port => ([a, b]) => a === port || b === port;
    const anotherPort = ([a, b], port) => (a === port ? b : a);
    const genBridges = function* (comps, used = [], lastPort = 0) {
        const matching = comps.filter(canConnect(lastPort));
        if (!matching.length) yield [...used];
        for (const comp of matching) {
            const i = comps.indexOf(comp);
            const [next] = comps.splice(i, 1);
            used.push(next);
            yield* genBridges(comps, used, anotherPort(next, lastPort));
            comps.splice(i, 0, next);
            used.pop();
        }
    };

    const strength = bridge => bridge.reduce((n, [a, b]) => n + a + b, 0);
    const maxBy = f => arr => arr.reduce((max, x) => Math.max(max, f(x)), 0);
    const longest = bridges => {
        const maxLen = maxBy(bridge => bridge.length)(bridges);
        return bridges.filter(bridge => bridge.length === maxLen);
    };

    const input = document.body.textContent.trim().split('\n');
    const components = input.map(s => s.split('/').map(Number));
    const bridges = [...genBridges(components)];
    console.log([bridges, longest(bridges)].map(maxBy(strength))); // 4.5 sec
}
