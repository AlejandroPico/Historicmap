export type Appearance='morning'|'afternoon'|'night'|'auto';
export type ResolvedAppearance=Exclude<Appearance,'auto'>;
export const appearances:Appearance[]=['morning','afternoon','night','auto'];
export const appearanceLabels:Record<Appearance,string>={morning:'Mañana',afternoon:'Tarde',night:'Noche',auto:'Automático'};
export const appearanceIcons:Record<Appearance,string>={morning:'sun',afternoon:'sunset',night:'moon',auto:'contrast'};
export const palettes:Record<ResolvedAppearance,{background:string;ocean:string;horizon:string}>={
  morning:{background:'#b9cbd0',ocean:'#d4e4e8',horizon:'#dbe8e8'},
  afternoon:{background:'#263139',ocean:'#3d515b',horizon:'#a79d89'},
  night:{background:'#080f19',ocean:'#152b3b',horizon:'#566b7e'},
};
/** Device-local time; no location, permission or network clock is required. */
export function resolveAppearance(mode:Appearance,now=new Date()):ResolvedAppearance{
  if(mode!=='auto')return mode;
  const hour=now.getHours();return hour>=7&&hour<13?'morning':hour>=13&&hour<20?'afternoon':'night';
}
export function storedAppearance():Appearance{
  try{const value=localStorage.getItem('historicmap-appearance');return appearances.includes(value as Appearance)?value as Appearance:'auto';}catch{return 'auto';}
}
