'use strict';

{
    const part1 = x => (x - 2) ** 2;
    const part2 = x => {
        let divisors = 0;
        let step = 1;
        while (step++ <= 1001) {
            let d = 2;
            while (x % d !== 0) d++;
            if (x !== d) divisors++;
            x += 17;
        }

        return divisors;
    };

    console.log(part1(65)); // the first number in the input
    console.log(part2(65 * 100 + 100000));
}
