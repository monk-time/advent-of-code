'use strict';

{
    const unzipLen = (s, rec = false) => {
        let [sum, i] = [0, 0];
        while (i < s.length) {
            if (s[i] !== '(') {
                [sum, i] = [sum + 1, i + 1];
                continue;
            }

            const [m, next, repeat] = s.slice(i).match(/\((\d+)x(\d+)\)/);
            const sectEnd = i + m.length + +next;
            const sectLen = +repeat *
                (rec ? unzipLen(s.slice(i + m.length, sectEnd), rec) : +next);
            [sum, i] = [sum + sectLen, sectEnd];
        }

        return sum;
    };

    const input = document.body.textContent.trim();
    console.log(unzipLen(input), unzipLen(input, true));
}

{
    // Alternative solution without loops.
    // Credit: https://www.reddit.com/r/adventofcode/comments/5hbygy/2016_day_9_solutions/daz2o0d/
    const unzipLen = (s, rec = false, sum = 0) => {
        const { 0: m, 1: next, 2: times, index } = /\((\d+)x(\d+)\)/g.exec(s) || [];
        if (!m) return sum + s.length;
        const sectEnd = index + m.length + +next;
        const sectLen = +times *
            (rec ? unzipLen(s.slice(sectEnd - +next, sectEnd), rec) : +next);
        return unzipLen(s.slice(sectEnd), rec, sum + index + sectLen);
    };

    const input = document.body.textContent.trim();
    console.log(unzipLen(input), unzipLen(input, true));
}
