const value = JSON.parse(document.getElementById('kanji-data').textContent);
const forConvert = "\"" + value.substring(1, value.length - 1) + "\"";

const kanjiList = JSON.parse(value);
console.log(kanjiList);