'use strict';
let input = document.querySelector('pre').textContent.trim(),
    start = [0, 0],
    moveX = dx => ([x, y]) => [x + dx, y],
    moveY = dy => ([x, y]) => [x, y + dy];

let moveMap = {
    '^': moveY(1), 'v': moveY(-1), // jscs:ignore disallowQuotedKeysInObjects
    '>': moveX(1), '<': moveX(-1)
};

// if a set is passed, it is mutated; otherwise a new set is returned
function travel(path, visited = new Set([start.join()])) {
    path.reduce((house, char) => {
        house = moveMap[char](house);
        visited.add(house.join()); // Set compares values by ===
        return house;
    }, start);

    return visited;
}

function splitInTwo(str) {
    let [a, b] = [[], []];
    [...str].forEach((ch, i) => (i % 2 === 0 ? a : b).push(ch));
    return [a, b];
}

let visitedBySanta = travel([...input]);
console.log(`Houses visited by Santa: ${visitedBySanta.size}`);

let [santaPath, roboPath] = splitInTwo(input),
    visitedBySanta2 = travel(santaPath),
    visitedByBoth   = travel(roboPath, visitedBySanta2);
console.log(`Houses visited by Santa and Robo-Santa: ${visitedByBoth.size}`);
