"""Named sixteenth-century office research; candidates require explicit review."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
r.GROUPS=[
 ('FRA','Rey de Francia',['Louis XII','Francis I of France','Henry II of France','Francis II of France','Charles IX of France','Henry III of France','Henry IV of France']),
 ('CASTILE','Reina / rey de Castilla',['Isabella I of Castile','Joanna of Castile','Philip I of Castile','Charles V, Holy Roman Emperor']),
 ('ARAGON','Rey de Aragón',['Ferdinand II of Aragon','Charles V, Holy Roman Emperor']),
 ('ESP','Rey de la monarquía hispánica',['Charles V, Holy Roman Emperor','Philip II of Spain','Philip III of Spain']),
 ('PRT','Rey de Portugal',['Manuel I of Portugal','John III of Portugal','Sebastian of Portugal','Henry, King of Portugal','Philip II of Spain','Philip III of Spain']),
 ('ENGLAND','Rey / reina de Inglaterra',['Henry VII of England','Henry VIII','Edward VI','Lady Jane Grey','Mary I of England','Elizabeth I']),
 ('SCOTLAND','Rey / reina de Escocia',['James IV of Scotland','James V of Scotland','Mary, Queen of Scots','James VI and I']),
 ('HIST-Q12548','Emperador del Sacro Imperio',['Maximilian I, Holy Roman Emperor','Charles V, Holy Roman Emperor','Ferdinand I, Holy Roman Emperor','Maximilian II, Holy Roman Emperor','Rudolf II, Holy Roman Emperor']),
 ('BAVARIA-DUCHY','Duque de Baviera',['Albert IV, Duke of Bavaria','William IV, Duke of Bavaria','Louis X, Duke of Bavaria','Albert V, Duke of Bavaria','William V, Duke of Bavaria','Maximilian I, Elector of Bavaria']),
 ('SAXONY-ELECTORATE','Elector de Sajonia',['Frederick III, Elector of Saxony','John, Elector of Saxony','John Frederick I, Elector of Saxony','Maurice, Elector of Saxony','Augustus, Elector of Saxony','Christian I, Elector of Saxony','Christian II, Elector of Saxony']),
 ('HESSE-UNITED','Landgrave de Hesse',['William II, Landgrave of Hesse','Philip I, Landgrave of Hesse']),
 ('HESSE-KASSEL','Landgrave de Hesse-Kassel',['William IV, Landgrave of Hesse-Kassel','Maurice, Landgrave of Hesse-Kassel']),
 ('HESSE-DARMSTADT','Landgrave de Hesse-Darmstadt',['George I, Landgrave of Hesse-Darmstadt','Louis V, Landgrave of Hesse-Darmstadt']),
 ('WURTTEMBERG-DUCHY','Duque de Wurtemberg',['Ulrich, Duke of Württemberg','Christoph, Duke of Württemberg','Louis III, Duke of Württemberg','Frederick I, Duke of Württemberg']),
 ('ELECTORATE-BRANDENBURG','Elector de Brandeburgo',['Joachim I Nestor, Elector of Brandenburg','Joachim II Hector, Elector of Brandenburg','John George, Elector of Brandenburg','Joachim Frederick, Elector of Brandenburg']),
 ('PRUSSIA-DUCHY','Duque de Prusia',['Albert, Duke of Prussia','Albert Frederick, Duke of Prussia']),
 ('MUSCOVY','Gran príncipe de Moscú',['Ivan III of Russia','Vasili III of Russia','Ivan the Terrible']),
 ('RUSSIA-TSARDOM','Zar de Rusia',['Ivan the Terrible','Feodor I of Russia','Boris Godunov']),
 ('OTT','Sultán otomano',['Bayezid II','Selim I','Suleiman the Magnificent','Selim II','Murad III','Mehmed III']),
 ('SAFAVID','Shah safávida',['Ismail I','Tahmasp I','Ismail II','Mohammad Khodabanda','Abbas the Great']),
 ('MING','Emperador Ming',['Hongzhi Emperor','Zhengde Emperor','Jiajing Emperor','Longqing Emperor','Wanli Emperor']),
 ('HIST-Q33296','Emperador mogol',['Babur','Humayun','Akbar']),
 ('SUR','Soberano surí',['Sher Shah Suri','Islam Shah Suri','Firuz Shah Suri','Muhammad Adil Shah','Sikandar Shah Suri']),
 ('JOS','Rey de Joseon',['Yeonsangun of Joseon','Jungjong of Joseon','Injong of Joseon','Myeongjong of Joseon','Seonjo of Joseon']),
 ('JPN','Emperador · corte imperial',['Emperor Go-Kashiwabara','Emperor Go-Nara','Emperor Ōgimachi','Emperor Go-Yōzei']),
 ('JPN','Shogun Ashikaga · autoridad militar',['Ashikaga Yoshitane','Ashikaga Yoshizumi','Ashikaga Yoshiharu','Ashikaga Yoshiteru','Ashikaga Yoshihide','Ashikaga Yoshiaki']),
 ('JPN','Dirigente político-militar · ámbito de consolidación',['Oda Nobunaga','Toyotomi Hideyoshi']),
 ('AZTEC','Huey tlatoani · autoridad mexica',['Ahuitzotl','Moctezuma II','Cuitláhuac','Cuauhtémoc']),
 ('INCA','Sapa Inca',['Huayna Capac','Huáscar','Atahualpa','Túpac Huallpa','Manco Inca Yupanqui']),
 ('NEO-INCA','Soberano de Vilcabamba',['Manco Inca Yupanqui','Sayri Túpac','Titu Cusi','Túpac Amaru']),
 ('ETH','Emperador de Etiopía',['Naod','Dawit II','Gelawdewos','Menas of Ethiopia','Sarsa Dengel','Yaqob']),
 ('HIST-Q796583','Rey del Kongo',['Manuel I of Kongo','Afonso I of Kongo','Pedro I of Kongo','Francisco I of Kongo','Diogo I of Kongo','Afonso II of Kongo','Bernardo I of Kongo','Henrique I of Kongo','Álvaro I of Kongo','Álvaro II of Kongo']),
 ('HIST-Q202687','Askia · soberano de Songhai',['Askia Mohammad I','Askia Musa','Askia Mohammad II','Askia Ismail','Askia Ishaq I','Askia Daoud','Askia Mohammad III','Askia Mohammad IV Bano','Askia Ishaq II']),
 ('SAVOY-DUCHY','Duque de Saboya',['Philibert II, Duke of Savoy','Charles III, Duke of Savoy','Emmanuel Philibert, Duke of Savoy','Charles Emmanuel I, Duke of Savoy'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index("if __name__")].replace('core019-rulers.json','rulers021-candidates.json').replace('core019meta-','rulers021meta-');exec(compile(code,'rulers021','exec'),r.__dict__)
if __name__=='__main__':r.main()
