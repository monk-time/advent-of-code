'use strict';

{
    const unzipLen = (s, rec = false) => {
        let [sum, i] = [0, 0];
        while (i < s.length) {
            if (s[i] !== '(') {
                [sum, i] = [sum + 1, i + 1];
                continue;
            }
            const [m, next, repeat] = s.slice(i).match(/\((\d+)x(\d+)\)/),
                sectEnd = i + m.length + (+next),
                sectLen = (+repeat) * (rec ? unzipLen(s.slice(i + m.length, sectEnd), rec) : +next);
            [sum, i] = [sum + sectLen, sectEnd];
        }

        return sum;
    };

    const input = document.body.textContent.trim();
    console.log(unzipLen(input), unzipLen(input, true));
}
