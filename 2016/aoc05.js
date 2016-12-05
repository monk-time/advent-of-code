'use strict';

{
    const input = document.body.textContent,
        main = () => console.log(password8('ffykfhsq'));
    
    const password8 = function (salt) {
        let [passLen, i, pass] = [0, 0, Array(8)];
        while (passLen < 8) {
            let hash = md5(salt + i++);
            if (hash.startsWith('00000')) {
                let [pos, ch] = [+hash[5], hash[6]];
                if ((pos < 8) && (pass[pos] === undefined)) {
                    passLen++;
                    pass[pos] = ch;
                }
            }
        }
        return pass.join('');
    }

    fetch('//cdn.jsdelivr.net/js-md5/0.4.1/md5.min.js')
        .then(r => r.text()).then(eval).then(main);
}
