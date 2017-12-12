'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const freq = a => el => a.filter(x => x === el).length;
    const freqSort = a => [...new Set(a)].sort((x, y) => freq(a)(x) - freq(a)(y));
    const cols = as => [...as[0]].map((_, i) => as.map(a => a[i]));
    const sortByCol = as => cols(as).map(freqSort);
    const heads = as => fromEnd => as.map(a => a[fromEnd ? a.length - 1 : 0]).join('');
    console.log(...[true, false].map(heads(sortByCol(input))));
}
