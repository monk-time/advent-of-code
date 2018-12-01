'use strict';

{
    const input = document.body.textContent.trim();
    console.log([...input].reduce(({ floor = 0, basement }, paren, pos) => {
        floor += paren === '(' ? 1 : paren === ')' ? -1 : 0;
        if (floor === -1 && !basement) basement = pos + 1;
        return { floor, basement };
    }, {}));
}
