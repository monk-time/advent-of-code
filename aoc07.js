'use strict';
function parse(line) {
    let [cmd, id] = line.split(' -> '),
        [op] = cmd.match(/[A-Z]+/) || [],
        [x, y] = cmd.match(/[a-z]+|\d+/g); // y may be undefined
    return { [id]: { x, y, op: op || 'PUT' } };
}

let ops = {
    PUT: x => +x,
    NOT: x => ~x & 0xFFFF, // signal must be positive and 16-bit
    AND: (x, y) => x & y,
    OR:  (x, y) => x | y,
    LSHIFT: (x, y) => x << y & 0xFFFF,
    RSHIFT: (x, y) => x >>> y
};

function signal(circuit, id) {
    let wire = circuit[id];
    if (wire === undefined) return +id; // op arg was a number, not a wire id
    if (wire.val === undefined) {
        let x = signal(circuit, wire.x),
            y = wire.y && signal(circuit, wire.y); // some ops are unary
        wire.val = ops[wire.op](x, y);
    }

    return wire.val;
}

let input = document.body.textContent.trim().split('\n'),
    getCircuit = booklet => Object.assign({}, ...booklet.map(parse));

let a = signal(getCircuit(input), 'a');
console.log('Part 1:', a);
let newCircuit = getCircuit(input);
newCircuit.b.val = a;
console.log('Part 2:', signal(newCircuit, 'a'));
