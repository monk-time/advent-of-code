// JavaScript (ES2015) with [emn178's js-md5 library](https://www.npmjs.com/package/js-md5).
// A lot of boilerplate to load a third-party lib in browser and be able to change md5 library.
// Average exec. time (i7-4710HQ): 1.9 sec in FF42 (Scratchpad), 2.1 sec in Chrome 47 (Snippets).

'use strict';
let md5lib = {
    url: 'https://rawgit.com/emn178/js-md5/master/src/md5.js',
    isLoaded: () => typeof md5 !== 'undefined',
    md5: s => md5(s),
};

function loadScript(url, callback) {
    let script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.onload = callback;
    document.getElementsByTagName('head')[0].appendChild(script);
}

function mine(key) {
    let n = 0,
        hash = '';
    for (let zn of [5, 6]) {
        let zeroes = '0'.repeat(zn);
        while (hash.substring(0, zn) !== zeroes) {
            hash = md5lib.md5(key + (++n));
        }

        console.log(`Answer (${zn} zeroes): ${n} for key ${key} and hash ${hash}`);
    }
}

function solve() {
    let input = document.querySelector('pre').textContent.trim();
    console.time('main');
    mine(input);
    console.timeEnd('main');
}

function main() {
    if (md5lib.isLoaded()) {
        solve();
    } else {
        loadScript(md5lib.url, solve);
    }
}

main();
