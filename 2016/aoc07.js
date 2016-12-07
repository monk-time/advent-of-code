'use strict';

{
    const [supernet, hypernet] = [0, 1].map(mod =>
        ip => ip.split(/\[(.+?)\]/g).filter((_, i) => i % 2 === mod).join('-'));
    const matchEnds = function* (re, s) {
        if (re.exec(s) === null) return;
        yield re.lastIndex - 1;
        yield* matchEnds(re, s);
    };
    const input = document.body.textContent.trim().split('\n'),
        abbas = s => s.match(/(.)((?!\1).)\2\1/g) || [],
        abas = s => [...matchEnds(/(.)(?!\1)(?=.\1)/g, s)].map(i => s[i] + s[i + 1]),
        hasTLS = ip => abbas(supernet(ip)).length > 0 && abbas(hypernet(ip)).length === 0,
        hasSSL = ip => abas(supernet(ip)).some(s => abas(hypernet(ip)).includes(s[1] + s[0]));

    console.log(...[hasTLS, hasSSL].map(f => input.filter(f).length));
}
