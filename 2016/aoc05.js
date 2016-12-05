'use strict';

{
    const [input, cache] = ['ffykfhsq', []],
        getHash = n => md5(input + n);
    const hashes5x0 = function* () {
        yield* cache.map(getHash);
        let i = cache.length ? cache[cache.length - 1] : -1;
        while (true) {
            const hash = getHash(++i);
            if (hash.startsWith('00000')) {
                cache.push(i);
                yield hash;
            }
        }
    };
    const updateL = (arr, pos, val) => arr.map((x, i) => i === pos ? val : x);
    const algs = [
        (pass, hash) => updateL(pass, pass.indexOf(undefined), hash[5]),
        (pass, hash) => {
            const pos = +hash[5]; // NaN if in a..e
            return pos < 8 && pass[pos] === undefined ?
                updateL(pass, pos, hash[6]) : pass;
        }
    ];
    const password = alg => {
        let pass = [...new Array(8)];
        for (let hash of hashes5x0()) {
            pass = alg(pass, hash);
            if (!pass.includes(undefined)) {
                return pass.join('');
            }
        }
    };

    const main = () => console.log(...algs.map(password));
    fetch('//cdn.jsdelivr.net/js-md5/0.4.1/md5.min.js')
        .then(r => r.text()).then(eval).then(main);
}
