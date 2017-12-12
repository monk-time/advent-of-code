'use strict';

{
    const [supernet, hypernet] = [0, 1].map(mod =>
        ip => ip.split(/\[(.+?)\]/g).filter((_, i) => i % 2 === mod).join('-'));
    const matchAll = function* (re, s, m = re.exec(s)) { // all group 1 matches
        if (m === null) return;
        yield m[1];
        yield* matchAll(re, s);
    };

    const input = document.body.textContent.trim().split('\n');
    const abbas = s => s.match(/(.)((?!\1).)\2\1/g) || [];
    const abas = s => [...matchAll(/(?=((.)(?!\2).)\2)./g, s)];
    const hasTLS = ip => abbas(supernet(ip)).length > 0 && abbas(hypernet(ip)).length === 0;
    const hasSSL = ip => abas(supernet(ip)).some(s => abas(hypernet(ip)).includes(s[1] + s[0]));

    console.log(...[hasTLS, hasSSL].map(f => input.filter(f).length));
}
