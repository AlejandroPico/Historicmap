"""Named fifteenth-century authorities: review offices, not birth/death dates."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
r.GROUPS=[
 ('FRA','Rey de Francia',['Charles VI of France','Charles VII of France','Louis XI','Charles VIII of France','Louis XII']),
 ('CASTILE','Rey / reina de Castilla',['Henry III of Castile','John II of Castile','Henry IV of Castile','Isabella I of Castile']),
 ('ARAGON','Rey de Aragón',['Martin of Aragon','Ferdinand I of Aragon','Alfonso V of Aragon','John II of Aragon','Ferdinand II of Aragon']),
 ('PRT','Rey de Portugal',['John I of Portugal','Edward, King of Portugal','Afonso V of Portugal','John II of Portugal','Manuel I of Portugal']),
 ('ENGLAND','Rey de Inglaterra',['Henry IV of England','Henry V of England','Henry VI of England','Edward IV','Edward V','Richard III of England','Henry VII of England']),
 ('SCOTLAND','Rey de Escocia',['Robert III of Scotland','James I of Scotland','James II of Scotland','James III of Scotland','James IV of Scotland']),
 ('HIST-Q12548','Rey de Romanos / emperador',['Wenceslaus IV of Bohemia','Rupert, King of Germany','Sigismund, Holy Roman Emperor','Albert II of Germany','Frederick III, Holy Roman Emperor','Maximilian I, Holy Roman Emperor']),
 ('BURGUNDY-DUCHY','Duque / duquesa de Borgoña',['Philip the Bold','John the Fearless','Philip the Good','Charles the Bold','Mary of Burgundy']),
 ('NAVARRE-KINGDOM','Rey / reina de Navarra',['Charles III of Navarre','Blanche I of Navarre','John II of Aragon','Eleanor of Navarre','Francis Phoebus','Catherine of Navarre']),
 ('BYZANTINE','Emperador bizantino',['Manuel II Palaiologos','John VIII Palaiologos','Constantine XI Palaiologos']),
 ('TREBIZOND','Emperador de Trebisonda',['Manuel III of Trebizond','Alexios IV of Trebizond','John IV of Trebizond','David of Trebizond']),
 ('OTT','Sultán otomano',['Bayezid I','Mehmed I','Murad II','Mehmed II','Bayezid II']),
 ('MUSCOVY','Gran príncipe de Moscú',['Vasily I of Moscow','Vasily II of Moscow','Ivan III of Russia']),
 ('POLAND-KINGDOM','Rey de Polonia',['Władysław II Jagiełło','Władysław III of Poland','Casimir IV Jagiellon','John I Albert']),
 ('LITHUANIA-DUCHY','Gran duque de Lituania',['Vytautas','Švitrigaila','Sigismund Kęstutaitis','Casimir IV Jagiellon','Alexander Jagiellon']),
 ('KALMAR','Autoridad de la unión de Kalmar',['Margaret I of Denmark','Eric of Pomerania','Christopher of Bavaria','Christian I of Denmark','John, King of Denmark']),
 ('MING','Emperador Ming',['Jianwen Emperor','Yongle Emperor','Hongxi Emperor','Xuande Emperor','Emperor Yingzong of Ming','Jingtai Emperor','Chenghua Emperor','Hongzhi Emperor']),
 ('JOS','Rey de Joseon',['Jeongjong of Joseon','Taejong of Joseon','Sejong the Great','Munjong of Joseon','Danjong','Sejo of Joseon','Yejong of Joseon','Seongjong of Joseon','Yeonsangun of Joseon']),
 ('JPN','Emperador · corte imperial',['Emperor Go-Komatsu','Emperor Shōkō','Emperor Go-Hanazono','Emperor Go-Tsuchimikado']),
 ('JPN','Shogun Ashikaga',['Ashikaga Yoshimitsu','Ashikaga Yoshimochi','Ashikaga Yoshikazu','Ashikaga Yoshinori','Ashikaga Yoshikatsu','Ashikaga Yoshimasa','Ashikaga Yoshihisa','Ashikaga Yoshitane','Ashikaga Yoshizumi']),
 ('TIMURID','Soberano timúrida · ámbito regional',['Timur','Shah Rukh','Ulugh Beg','Abu Sa\'id Mirza','Sultan Husayn Bayqara']),
 ('AZTEC','Huey tlatoani',['Itzcoatl','Moctezuma I','Axayacatl','Tizoc','Ahuitzotl']),
 ('INCA','Sapa Inca · cronología tradicional',['Pachacuti','Topa Inca Yupanqui','Huayna Capac']),
 ('MAMLUKS','Sultán mameluco',['Barquq','An-Nasir Faraj','Al-Mu\'ayyad Shaykh','Barsbay','Jaqmaq','Inal','Qaitbay']),
 ('HESSE-UNITED','Landgrave de Hesse',['Hermann II, Landgrave of Hesse','Louis I, Landgrave of Hesse','Louis II, Landgrave of Hesse','Henry III, Landgrave of Upper Hesse','William I, Landgrave of Lower Hesse','William III, Landgrave of Upper Hesse','William II, Landgrave of Hesse']),
 ('SAXONY-ELECTORATE','Elector de Sajonia',['Rudolf III, Duke of Saxe-Wittenberg','Albert III, Duke of Saxe-Wittenberg','Frederick I, Elector of Saxony','Frederick II, Elector of Saxony','Ernest, Elector of Saxony','Frederick III, Elector of Saxony']),
 ('ELECTORATE-BRANDENBURG','Elector de Brandeburgo',['Jobst of Moravia','Frederick I, Elector of Brandenburg','Frederick II, Elector of Brandenburg','Albrecht III Achilles, Elector of Brandenburg','John Cicero, Elector of Brandenburg','Joachim I Nestor, Elector of Brandenburg']),
 ('SAVOY-DUCHY','Conde / duque de Saboya',['Amadeus VIII, Duke of Savoy','Louis, Duke of Savoy','Amadeus IX, Duke of Savoy','Philibert I, Duke of Savoy','Charles I, Duke of Savoy','Charles II, Duke of Savoy','Philip II, Duke of Savoy','Philibert II, Duke of Savoy']),
 ('WURTTEMBERG-DUCHY','Conde / duque de Wurtemberg',['Eberhard III, Count of Württemberg','Eberhard IV, Count of Württemberg','Ludwig I, Count of Württemberg-Urach','Ulrich V, Count of Württemberg','Eberhard I, Duke of Württemberg','Eberhard II, Duke of Württemberg','Ulrich, Duke of Württemberg']),
 ('ETH','Emperador de Etiopía',['Dawit I','Yeshaq I','Zara Yaqob','Baeda Maryam I','Eskender','Na\'od']),
 ('HIST-Q796583','Rey del Kongo',['João I of Kongo']),
 ('GRANADA-EMIRATE','Emir nazarí',['Muhammad VII of Granada','Yusuf III of Granada','Muhammad IX of Granada','Abu l-Hasan Ali, Sultan of Granada','Muhammad XII of Granada','Muhammad XIII of Granada'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index('if __name__')].replace('core019-rulers.json','rulers022-candidates.json').replace('core019meta-','rulers022meta-');exec(compile(code,'rulers022','exec'),r.__dict__)
if __name__=='__main__':r.main()
