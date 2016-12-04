'use strict';

{
    const input = document.body.textContent.trim().split('\n'),
        re = /([a-z-]+)-(\d+)\[([a-z]+)\]/,
        parse = s => (([, name, id, crc]) => ({ name, id: +id, crc }))(s.match(re)),
        freq = (a, el) => a.filter(x => x === el).length,
        common5 = a => [...new Set(a)].sort().sort((x, y) => freq(a, y) - freq(a, x)).slice(0, 5),
        isReal = r => common5([...r.name.replace(/-/g, '')]).join('') === r.crc,
        shiftChar = n => ch => String.fromCharCode(97 + (ch.charCodeAt() - 97 + n) % 26),
        shift = n => s => s.replace(/./g, shiftChar(n)),
        decrypt = ({ name, id }) => ({ name: name.split('-').map(shift(id)).join(' '), id }),
        sumID = rs => rs.reduce((sum, r) => sum + r.id, 0),
        poleID = rs => rs.map(decrypt).find(r => r.name.includes('pole')).id,
        realRooms = input.map(parse).filter(isReal);

    console.log(sumID(realRooms), poleID(realRooms));
}
