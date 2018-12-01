'use strict';

{
    const part1 = x => (x - 2) ** 2;
    const part2 = x => {
        let nonprimes = 0;
        for (let n = x; n <= x + 17000; n += 17) {
            let d = 2;
            while (n % d !== 0) d++;
            if (n !== d) nonprimes++;
        }

        return nonprimes;
    };

    const input = +document.body.textContent.match(/\d+/)[0]; // the first number
    console.log(part1(input), part2(input * 100 + 100000));
}
