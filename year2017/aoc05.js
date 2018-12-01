'use strict';

{
    const stepsToExit = offsetsStart => jump => {
        const offsets = [...offsetsStart];
        let [pointer, i] = [0, 0];
        while (++i) {
            const o = offsets[pointer];
            offsets[pointer] += jump(o);
            pointer += o;
            if (pointer < 0 || pointer >= offsets.length) return i;
        }
    };

    const offsets = document.body.textContent.trim().split('\n').map(Number);
    console.log([() => 1, d => (d >= 3 ? -1 : 1)].map(stepsToExit(offsets)));
}
