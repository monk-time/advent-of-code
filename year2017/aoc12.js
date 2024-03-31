// https://adventofcode.com/2017/day/12

'use strict';

{
    const findGroupWith = (head, pipes) => {
        const [queue, group] = [[head], new Set([head])];
        while (queue.length) {
            pipes[queue.pop()].forEach(p => {
                if (group.has(p)) return;
                group.add(p);
                queue.push(p);
            });
        }

        return group;
    };

    const allGroups = pipes => {
        const groups = [];
        let pipesToCheck = [...pipes.keys()].reverse();
        while (pipesToCheck.length) {
            const group = findGroupWith(pipesToCheck.pop(), pipes);
            groups.push(group);
            pipesToCheck = pipesToCheck.filter(p => !group.has(p));
        }

        return groups;
    };

    const input = document.body.textContent.trim();
    const pipes = input.split('\n').map(s => s.match(/\d+/g).map(Number).slice(1));
    const groups = allGroups(pipes);
    console.log(groups[0].size, groups.length);
}
