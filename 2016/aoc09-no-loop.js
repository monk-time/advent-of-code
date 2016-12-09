'use strict';
// credit: https://www.reddit.com/r/adventofcode/comments/5hbygy/2016_day_9_solutions/daz2o0d/

{
    const unzipLen = (s, rec = false, sum = 0) => {
        const { 0: m, 1: next, 2: times, index } = /\((\d+)x(\d+)\)/g.exec(s) || [];
        if (!m) return sum + s.length;
        const sectEnd = index + m.length + (+next),
              sectLen = +times * (rec ? unzipLen(s.slice(sectEnd - +next, sectEnd), rec) : +next);
        return unzipLen(s.slice(sectEnd), rec, sum + index + sectLen);
    };

    const input = document.body.textContent.trim();
    console.log(unzipLen(input), unzipLen(input, true));
}
