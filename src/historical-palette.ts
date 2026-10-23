/** Editorial cartographic conventions, not historical state-owned colours or ideology.
 * Named entities resolve their own family; regime chronology stays in political.ts.
 * The unavailable user CSV has NOT been imported or silently reconstructed.
 */
export const historicalPalette=[
 {key:'GBR',color:'#b2789b',names:['British Empire','Imperio británico']},
 {key:'USSR',color:'#c74743',names:['Soviet Union','Unión Soviética']},
 {key:'USA',color:'#4e89bd',names:['United States of America','Estados Unidos']},
 {key:'FRA-EMPIRE',color:'#387cc1',names:['First French Empire','Imperio napoleónico']},
 {key:'ESP-EMPIRE',color:'#c3a04f',names:['Spanish Empire','Imperio español']},
 {key:'DEU-NAZI',color:'#50545a',names:['Nazi Germany','Alemania nazi']},
 {key:'PRT-EMPIRE',color:'#638d73',names:['Portuguese Empire','Imperio portugués']},
 {key:'OTT',color:'#9b5b64',names:['Ottoman Empire','Imperio otomano']},
 {key:'ROME',color:'#8d3b68',names:['Roman Empire','Western Roman Empire','Imperio romano','Imperio Romano','Roma']},
 {key:'ROME-REPUBLIC',color:'#ad594f',names:['Roman Republic','República romana']},
 {key:'BYZANTIUM',color:'#70539c',names:['Eastern Roman Empire','Byzantine Empire','Imperio bizantino']},
 {key:'EGYPT-ANCIENT',color:'#c5a059',names:['Ancient Egypt','New Kingdom of Egypt','Middle Kingdom of Egypt','Old Kingdom of Egypt']},
 {key:'ACHAEMENID',color:'#409875',names:['Achaemenid Empire','Achaemenids','Persian Empire']},
 {key:'SASANIAN',color:'#925e9e',names:['Sasanian Empire','Sassanid Empire','Sassanids']},
 {key:'MACEDON',color:'#c9a448',names:['Macedonian Empire','Macedonia','Alexander the Great']},
 {key:'SELEUCID',color:'#587cae',names:['Seleucid Empire','Seleucids']},
 {key:'PTOLEMAIC',color:'#4f9b98',names:['Ptolemaic Kingdom','Ptolemaic Egypt']},
 {key:'MAURYA',color:'#c77e46',names:['Maurya Empire','Mauryan Empire']},
 {key:'GUPTA',color:'#c39f4c',names:['Gupta Empire']},
 {key:'MUGHAL',color:'#45845b',names:['Mughal Empire','Mughals']},
 {key:'QIN',color:'#555963',names:['Qin','Qin dynasty']},
 {key:'HAN',color:'#b65750',names:['Han','Han dynasty']},
 {key:'TANG',color:'#c4a45d',names:['Tang','Tang dynasty']},
 {key:'SONG',color:'#b4956b',names:['Song','Song dynasty']},
 {key:'MING',color:'#c89449',names:['Ming Empire','Ming dynasty']},
 {key:'MONGOL',color:'#7b8f9a',names:['Mongol Empire','Mongols']},
 {key:'UMAYYAD',color:'#519568',names:['Umayyad Caliphate','Umayyads']},
 {key:'ABBASID',color:'#53545c',names:['Abbasid Caliphate','Abbasids']},
 {key:'CAROLINGIAN',color:'#527ca8',names:['Carolingian Empire','Frankish Empire']},
 {key:'HOLY-ROMAN',color:'#b4a466',names:['Holy Roman Empire']},
 {key:'INCA',color:'#bc9c4c',names:['Inca Empire','Inca','Tawantinsuyu']},
 {key:'AZTEC',color:'#4b9991',names:['Aztec Empire','Aztec Triple Alliance']},
 {key:'KHMER',color:'#7c9b69',names:['Khmer Empire','Khmer']},
] as const;
export const historicalFamily=(name:string)=>historicalPalette.find(r=>(r.names as readonly string[]).includes(name))?.key;
export const historicalColor=(key:string)=>historicalPalette.find(r=>r.key===key)?.color;
