'use strict';

{
    const sumNumbers = o => part2 => {
        if (!(o instanceof Object)) return Number.isInteger(o) ? o : 0;
        if (!(o instanceof Array) && part2 && Object.values(o).includes('red')) return 0;
        return Object.values(o).reduce((sum, v) => sum + sumNumbers(v)(part2), 0);
    };

    const input = JSON.parse(document.body.textContent);
    console.log([false, true].map(sumNumbers(input)));
}
