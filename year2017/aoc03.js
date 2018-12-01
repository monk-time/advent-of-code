'use strict';

{
    /* eslint-disable no-multi-spaces */
    // Length of a side of the current ring
    const curR = i => (x => x + (1 - x % 2))(Math.ceil(Math.sqrt(i)));
    const steps = n => {
        const r = curR(n);
        const numR = (r - 1) / 2;
        const cycle = n - ((r - 2) ** 2);
        const innerOffset = cycle % (r - 1);

        return numR + Math.abs(innerOffset - numR);
    };

    // Hardcode 3x3 square to avoid corner cases where diagonals are too close
    const aSeq = [0, 1, 1, 2, 4, 5, 10, 11, 23, 25];
    const a = i => {
        if (i in aSeq) return aSeq[i];
        aSeq[i] = a(i - 1);

        const n = curR(i) - 2;   // the largest odd n so that n^2 < i,  or a side of a prev. ring
        const n2 = n ** 2;       // end of a previous ring
        const m2 = (n - 2) ** 2; // end of a ring before a prev. one
        const o2 = (n + 2) ** 2; // end of the current ring
        // Sides start after diagonals and end on them
        const placeOnSide = j => (j - n2) % (n + 1);
        // Number of the current side (1..4)
        const side = j => Math.ceil((j - n2) / (n + 1));
        // Go to the diagonal on this side and slide on it 1 step down to the center
        const downDiag = sideNum => m2 + sideNum * (n - 1);

        if (i === n2 + 1) { // start of a ring
            aSeq[i] += a(m2 + 1);
        } else if (i === o2 - 1) { // just before the end of a ring
            aSeq[i] += a(n2 - 1) + a(n2) + a(n2 + 1);
        } else if (i === o2) { // end of a ring
            aSeq[i] += a(n2) + a(n2 + 1);
        } else if (placeOnSide(i) === 0) { // on any of the 3 other diagonals
            aSeq[i] += a(downDiag(side(i)));
        } else if (placeOnSide(i) === n) { // before them
            const d = downDiag(side(i));
            aSeq[i] += a(d) + a(d - 1);
        } else if (placeOnSide(i) === 1) { // after them
            const d = downDiag(side(i - 1));
            aSeq[i] += a(d) + a(d + 1) + a(i - 2);
        } else { // just on a side, away from corners
            // Move one step vert./hor. closer to the center
            const j = downDiag(side(i) - 1) + placeOnSide(i) - 1;
            aSeq[i] += a(j - 1 === m2 ? n2 : j - 1) + a(j) + a(j + 1);
        }

        return aSeq[i];
    };

    const input = document.querySelector('.puzzle-input').textContent;
    console.log(steps(input));

    let [val, i] = [0, 0];
    while (val < input) val = a(++i);
    console.log(`a[${i}] = ${val}`);
}
