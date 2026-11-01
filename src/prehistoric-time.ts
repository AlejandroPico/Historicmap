/** Product consultation bounds, independent of annual political coverage. */
export const PREHISTORY_START=-7000000,PREHISTORY_END=-10001;
export const isPrehistoric=(y:number)=>Number.isInteger(y)&&y>=PREHISTORY_START&&y<=PREHISTORY_END;
