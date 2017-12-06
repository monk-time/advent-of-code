'use strict';

{
    const redistribute = a => (from => spread(a, from, ...div(a[from], a.length)))(maxIndex(a));
    const div = (x, y) => [Math.floor(x / y), x % y];
    const maxIndex = a => a.reduce((iMax, x, i) => (x > a[iMax] ? i : iMax), 0);
    const spread = (a, from, quot, rem) => a.map((x, i) =>
        (i === from ? 0 : x) + quot + (posAfter(i, from, a.length) < rem ? 1 : 0));
    const posAfter = (i, from, len) => (len + i - from - 1) % len;

    const findLoop = mem => {
        let [key, i] = [mem.toString(), 0];
        const cache = {};
        while (!(key in cache)) {
            cache[key] = i;
            mem = redistribute(mem);
            [key, i] = [mem.toString(), i + 1];
        }

        return [i, Object.keys(cache).length - cache[key]];
    };

    const input = document.body.textContent.trim().match(/\d+/g).map(Number);
    console.log(findLoop(input)); // 50 ms
}
