/* xlsx.js (C) 2013-present SheetJS -- http://sheetjs.com */
importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.14.1/shim.min.js');
/* uncomment the next line for encoding support */
importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.14.1/cpexcel.js');
importScripts('jszip.js');
importScripts('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.14.1/xlsx.js');
postMessage({t:"ready"});

onmessage = function (evt) {
  var v;
  try {
    v = XLSX.read(evt.data.d, {type: evt.data.b, cellDates:true, cellNF: false, cellText:false });
postMessage({t:"xlsx", d:JSON.stringify(v)});
  } catch(e) { postMessage({t:"e",d:e.stack||e}); }
};
