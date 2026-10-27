/** Lexically sortable positive historical years, including dates before1000. */
export function isoYear(year:number){return year<0?'-'+String(-year).padStart(4,'0'):String(year).padStart(4,'0');}
