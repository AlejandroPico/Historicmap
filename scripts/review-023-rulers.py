"""Fourteenth-century named office candidates; explicit review required."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
r.GROUPS=[
 ('FRA','Rey de Francia',['Philip IV of France','Louis X of France','John I of France','Philip V of France','Charles IV of France','Philip VI of France','John II of France','Charles V of France','Charles VI of France']),
 ('CASTILE','Rey / reina de Castilla',['Ferdinand IV of Castile','Alfonso XI of Castile','Peter of Castile','Henry II of Castile','John I of Castile','Henry III of Castile']),
 ('ARAGON','Rey de Aragón',['James II of Aragon','Alfonso IV of Aragon','Peter IV of Aragon','John I of Aragon','Martin of Aragon']),
 ('PRT','Rey de Portugal',['Denis of Portugal','Afonso IV of Portugal','Peter I of Portugal','Ferdinand I of Portugal','John I of Portugal']),
 ('ENGLAND','Rey de Inglaterra',['Edward I of England','Edward II of England','Edward III of England','Richard II of England','Henry IV of England']),
 ('SCOTLAND','Rey de Escocia',['John Balliol','Robert the Bruce','David II of Scotland','Edward Balliol','Robert II of Scotland','Robert III of Scotland']),
 ('NAVARRE-KINGDOM','Rey / reina de Navarra',['Joan I of Navarre','Louis X of France','John I of France','Philip V of France','Charles IV of France','Joan II of Navarre','Philip III of Navarre','Charles II of Navarre','Charles III of Navarre']),
 ('BYZANTINE','Emperador bizantino',['Andronikos II Palaiologos','Andronikos III Palaiologos','John V Palaiologos','John VI Kantakouzenos','Andronikos IV Palaiologos','John VII Palaiologos','Manuel II Palaiologos']),
 ('TREBIZOND','Emperador de Trebisonda',['Alexios II of Trebizond','Andronikos III of Trebizond','Manuel II of Trebizond','Basil of Trebizond','Irene Palaiologina of Trebizond','Anna Anachoutlou','John III of Trebizond','Michael of Trebizond','Alexios III of Trebizond','Manuel III of Trebizond']),
 ('OTT','Emir otomano',['Osman I','Orhan','Murad I','Bayezid I']),
 ('HIST-Q12548','Rey de Romanos / dignidad imperial',['Albert I of Germany','Henry VII, Holy Roman Emperor','Louis IV, Holy Roman Emperor','Charles IV, Holy Roman Emperor','Wenceslaus IV of Bohemia']),
 ('POLAND-MEDIEVAL','Rey de Polonia',['Wenceslaus II of Bohemia','Wenceslaus III of Bohemia','Władysław I Łokietek','Casimir III the Great','Louis I of Hungary','Jadwiga of Poland']),
 ('POLAND-KINGDOM','Rey de Polonia',['Władysław II Jagiełło','Jadwiga of Poland']),
 ('LITHUANIA-DUCHY','Gran duque de Lituania',['Vytenis','Gediminas','Jaunutis','Algirdas','Jogaila','Kęstutis','Vytautas']),
 ('MUSCOVY','Príncipe de Moscú',['Daniel of Moscow','Yury of Moscow','Ivan I of Moscow','Simeon of Moscow','Ivan II of Moscow','Dmitry Donskoy','Vasily I of Moscow']),
 ('YUAN','Emperador Yuan',['Temür Khan','Külüg Khan','Ayurbarwada Buyantu Khan','Gegeen Khan','Yesün Temür','Ragibagh Khan','Kusala','Jayaatu Khan Tugh Temür','Rinchinbal Khan','Toghon Temür']),
 ('MING','Emperador Ming',['Hongwu Emperor','Jianwen Emperor']),
 ('ILKHANATE','Ilkan · autoridad mongola de Persia',['Ghazan','Öljaitü','Abu Sa\'id Bahadur Khan','Arpa Ke\'un']),
 ('GOLDEN-HORDE','Khan de la Horda de Oro',['Tokhta','Öz Beg Khan','Jani Beg','Berdi Beg','Tokhtamysh']),
 ('TIMURID','Soberano timúrida',['Timur']),
 ('DELHI-KHALJI','Sultán de Delhi',['Alauddin Khalji','Shihabuddin Omar','Qutbuddin Mubarak Shah']),
 ('DELHI-TUGHLAQ','Sultán de Delhi',['Ghiyath al-Din Tughlaq','Muhammad bin Tughluq','Firuz Shah Tughlaq']),
 ('SERBIA-KINGDOM','Rey de Serbia',['Stefan Milutin','Stefan Dečanski','Stefan Dušan']),
 ('SERBIA-EMPIRE','Emperador serbio',['Stefan Dušan','Stefan Uroš V']),
 ('BOSNIA-BANATE','Ban de Bosnia',['Stephen I, Ban of Bosnia','Stephen II, Ban of Bosnia','Tvrtko I of Bosnia']),
 ('BOSNIA-KINGDOM','Rey de Bosnia',['Tvrtko I of Bosnia','Stephen Dabiša','Helen of Bosnia','Ostoja of Bosnia']),
 ('CILICIA-KINGDOM','Rey de Cilicia',['Hethum II of Armenia','Leo III, King of Armenia','Oshin, King of Armenia','Leo IV, King of Armenia','Constantine II, King of Armenia','Constantine III, King of Armenia','Constantine IV, King of Armenia','Leo V, King of Armenia']),
 ('HIST-Q184536','Mansa de Mali',['Mansa Musa','Mansa Suleyman']),
 ('MARINID','Sultán meriní',['Abu Yaqub Yusuf an-Nasr','Abu Thabit Amir','Abu al-Rabi Sulayman','Abu Sa\'id Uthman II','Abu al-Hasan Ali ibn Othman','Abu Inan Faris']),
 ('MAMLUKS','Sultán mameluco',['Al-Nasir Muhammad','Al-Mansur Abu Bakr','An-Nasir Ahmad','As-Salih Ismail','An-Nasir Hasan','Al-Ashraf Sha\'ban','Barquq']),
 ('GORYEO','Rey de Goryeo',['Chungnyeol of Goryeo','Chungseon of Goryeo','Chungsuk of Goryeo','Chunghye of Goryeo','Chungmok of Goryeo','Chungjeong of Goryeo','Gongmin of Goryeo','U of Goryeo','Chang of Goryeo','Gongyang of Goryeo']),
 ('JOS','Rey de Joseon',['Taejo of Joseon','Jeongjong of Joseon']),
 ('JPN','Emperador · corte imperial',['Emperor Go-Fushimi','Emperor Go-Nijō','Emperor Hanazono','Emperor Go-Daigo','Emperor Go-Murakami','Emperor Chōkei','Emperor Go-Kameyama','Emperor Kōgon','Emperor Kōmyō','Emperor Sukō','Emperor Go-Kōgon','Emperor Go-En\'yū','Emperor Go-Komatsu']),
 ('JPN','Shogun Ashikaga',['Ashikaga Takauji','Ashikaga Yoshiakira','Ashikaga Yoshimitsu']),
 ('ETH','Emperador de Etiopía',['Wedem Arad','Amda Seyon I','Newaya Krestos','Newaya Maryam','Dawit I']),
 ('SAVOY-COUNTY','Conde de Saboya',['Amadeus V, Count of Savoy','Edward, Count of Savoy','Aymon, Count of Savoy','Amadeus VI, Count of Savoy','Amadeus VII, Count of Savoy','Amadeus VIII, Duke of Savoy'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index('if __name__')].replace('core019-rulers.json','rulers023-candidates.json').replace('core019meta-','rulers023meta-');exec(compile(code,'rulers023','exec'),r.__dict__)
if __name__=='__main__':r.main()
