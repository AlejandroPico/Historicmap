/** Civil years: -0001 means 1 BCE, never astronomical year zero.
 * Signed dates are NOT lexically sortable. Use compareDates for intervals. */
export function isoYear(year:number){if(!Number.isInteger(year)||year===0)throw Error('Invalid civil year: '+year);return year<0?'-'+String(-year).padStart(4,'0'):String(year).padStart(4,'0');}
export function dateParts(value:string):[number,number,number]{
 const m=/^(-?\d{4,})-(\d{2})-(\d{2})$/.exec(value);
 if(!m||Number(m[1])===0)throw Error('Invalid civil date: '+value);
 return [Number(m[1]),Number(m[2]),Number(m[3])];
}
export const dateYear=(value:string)=>dateParts(value)[0];
export function compareDates(a:string,b:string){const x=dateParts(a),y=dateParts(b);return x[0]-y[0]||x[1]-y[1]||x[2]-y[2];}
