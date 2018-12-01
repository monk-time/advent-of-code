'use strict';

{
    const input = document.body.textContent.trim();
    const start = [0, 0];
    const moveX = dx => ([x, y]) => [x + dx, y];
    const moveY = dy => ([x, y]) => [x, y + dy];
    const movers = { '^': moveY(1), v: moveY(-1), '>': moveX(1), '<': moveX(-1) };

    // if a set is passed, it is mutated; otherwise a new set is returned
    const travel = (path, visited = new Set([start.join()])) => {
        path.reduce((house, char) => {
            house = movers[char](house);
            visited.add(house.join()); // Sets compare values by ===
            return house;
        }, start);

        return visited;
    };

    const splitInTwo = str => [0, 1].map(rem => [...str].filter((ch, i) => i % 2 === rem));

    const [santaPath, roboPath] = splitInTwo(input);
    const visitedBySanta  = travel([...input]);
    const visitedBySanta2 = travel(santaPath);
    const visitedByBoth   = travel(roboPath, visitedBySanta2);
    console.log(visitedBySanta.size, visitedByBoth.size);
}
