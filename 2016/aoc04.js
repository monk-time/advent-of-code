'use strict';

{
    const input = document.body.textContent.trim().split('\n');
    const re = /([a-z-]+)-(\d+)\[([a-z]+)\]/;
    const parse = s => (([, name, id, crc]) => ({ name, id: +id, crc }))(s.match(re));
    const freq = a => el => a.filter(x => x === el).length;
    const stableSort = f => (x, y) => f(y) - f(x) || x.localeCompare(y);
    const common5 = a => [...new Set(a)].sort(stableSort(freq(a))).slice(0, 5);
    const isReal = r => common5([...r.name.replace(/-/g, '')]).join('') === r.crc;
    const shiftChar = n => ch => String.fromCharCode(97 + (ch.charCodeAt() - 97 + n) % 26);
    const shift = n => s => s.replace(/./g, shiftChar(n));
    const decrypt = ({ name, id }) => ({ name: name.split('-').map(shift(id)).join(' '), id });
    const sumID = rs => rs.reduce((sum, r) => sum + r.id, 0);
    const poleID = rs => rs.map(decrypt).find(r => r.name.includes('pole')).id;
    const realRooms = input.map(parse).filter(isReal);

    console.log(sumID(realRooms), poleID(realRooms));
}
