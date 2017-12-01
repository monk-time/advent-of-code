'use strict';

{
    const parse = line => {
        const [cmd, id] = line.split(' -> ');
        const [op] = cmd.match(/[A-Z]+/) || [];
        const [x, y] = cmd.match(/[a-z]+|\d+/g); // y may be undefined
        return { [id]: { x, y, op: op || 'PUT' } };
    };

    /* eslint-disable no-bitwise */
    const ops = {
        PUT: x => +x,
        NOT: x => ~x & 0xFFFF, // signal must be positive and 16-bit
        AND: (x, y) => x & y,
        OR:  (x, y) => x | y,
        LSHIFT: (x, y) => x << y & 0xFFFF,
        RSHIFT: (x, y) => x >>> y,
    };

    const signal = (circuit, id) => {
        const wire = circuit[id];
        if (wire === undefined) return +id; // op arg was a number, not a wire id
        if (wire.val === undefined) {
            const x = signal(circuit, wire.x);
            const y = wire.y && signal(circuit, wire.y); // some ops are unary
            wire.val = ops[wire.op](x, y);
        }

        return wire.val;
    };

    const input = document.body.textContent.trim().split('\n');
    const getCircuit = booklet => Object.assign({}, ...booklet.map(parse));

    const a = signal(getCircuit(input), 'a');
    const newCircuit = getCircuit(input);
    newCircuit.b.val = a;
    console.log(a, signal(newCircuit, 'a'));
}
