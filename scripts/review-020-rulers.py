"""Named reign research; all office intervals retained for explicit review."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
r.GROUPS=[
 ('FRA','Rey de Francia',['Henry IV of France','Louis XIII','Louis XIV']),
 ('ESP','Rey de España',['Philip III of Spain','Philip IV of Spain','Charles II of Spain']),
 ('PRT','Rey de Portugal',['Philip III of Spain','Philip IV of Spain','John IV of Portugal','Afonso VI of Portugal','Peter II of Portugal']),
 ('ENGLAND','Rey / reina de Inglaterra',['Elizabeth I','James VI and I','Charles I of England','Charles II of England','James II of England','William III of England','Mary II of England']),
 ('SCOTLAND','Rey / reina de Escocia',['James VI and I','Charles I of England','Charles II of England','James II of England','William III of England','Mary II of England']),
 ('ENGLISH-COMMONWEALTH','Lord Protector',['Oliver Cromwell','Richard Cromwell']),
 ('HIST-Q12548','Emperador del Sacro Imperio',['Rudolf II, Holy Roman Emperor','Matthias, Holy Roman Emperor','Ferdinand II, Holy Roman Emperor','Ferdinand III, Holy Roman Emperor','Leopold I, Holy Roman Emperor']),
 ('SAXONY-ELECTORATE','Elector de Sajonia',['Christian II, Elector of Saxony','John George I, Elector of Saxony','John George II, Elector of Saxony','John George III, Elector of Saxony','John George IV, Elector of Saxony','Augustus II the Strong']),
 ('BAVARIA-ELECTORATE','Elector de Baviera',['Maximilian I, Elector of Bavaria','Ferdinand Maria, Elector of Bavaria','Maximilian II Emanuel, Elector of Bavaria']),
 ('ELECTORATE-BRANDENBURG','Elector de Brandeburgo',['Joachim Frederick, Elector of Brandenburg','John Sigismund, Elector of Brandenburg','George William, Elector of Brandenburg','Frederick William, Elector of Brandenburg','Frederick I of Prussia']),
 ('HESSE-KASSEL','Landgrave de Hesse-Kassel',['Maurice, Landgrave of Hesse-Kassel','William V, Landgrave of Hesse-Kassel','William VI, Landgrave of Hesse-Kassel','William VII, Landgrave of Hesse-Kassel','Charles I, Landgrave of Hesse-Kassel']),
 ('HESSE-DARMSTADT','Landgrave de Hesse-Darmstadt',['Louis V, Landgrave of Hesse-Darmstadt','Louis VI, Landgrave of Hesse-Darmstadt','Louis VII, Landgrave of Hesse-Darmstadt','Ernest Louis, Landgrave of Hesse-Darmstadt']),
 ('WURTTEMBERG-DUCHY','Duque de Wurtemberg',['Frederick I, Duke of Württemberg','John Frederick, Duke of Württemberg','Eberhard III, Duke of Württemberg','William Louis, Duke of Württemberg','Eberhard Louis, Duke of Württemberg']),
 ('DUTCH-REPUBLIC','Estatúder · cargo provincial',['Maurice, Prince of Orange','Frederick Henry, Prince of Orange','William II, Prince of Orange','William III of England']),
 ('RUSSIA-TSARDOM','Zar de Rusia',['Boris Godunov','Feodor II of Russia','False Dmitry I','Vasili IV of Russia','Michael of Russia','Alexis of Russia','Feodor III of Russia','Ivan V of Russia','Peter the Great']),
 ('OTT','Sultán otomano',['Mehmed III','Ahmed I','Mustafa I','Osman II','Murad IV','Ibrahim of the Ottoman Empire','Mehmed IV','Suleiman II','Ahmed II','Mustafa II']),
 ('SAFAVID','Shah safávida',['Abbas the Great','Safi of Persia','Abbas II of Persia','Suleiman I of Persia','Sultan Husayn']),
 ('MING','Emperador Ming',['Wanli Emperor','Taichang Emperor','Tianqi Emperor','Chongzhen Emperor']),
 ('SOUTHERN-MING','Emperador Ming del Sur',['Hongguang Emperor','Longwu Emperor','Shaowu Emperor','Yongli Emperor']),
 ('LATER-JIN','Khan de Jin posterior',['Nurhaci','Hong Taiji']),
 ('QING','Emperador Qing',['Hong Taiji','Shunzhi Emperor','Kangxi Emperor']),
 ('JPN','Emperador / emperatriz · corte imperial',['Emperor Go-Yōzei','Emperor Go-Mizunoo','Empress Meishō','Emperor Go-Kōmyō','Emperor Go-Sai','Emperor Reigen','Emperor Higashiyama']),
 ('JPN','Shogun · Gobierno militar',['Tokugawa Ieyasu','Tokugawa Hidetada','Tokugawa Iemitsu','Tokugawa Ietsuna','Tokugawa Tsunayoshi']),
 ('JOS','Rey de Joseon',['Seonjo of Joseon','Gwanghaegun of Joseon','Injo of Joseon','Hyojong of Joseon','Hyeonjong of Joseon','Sukjong of Joseon']),
 ('HIST-Q33296','Emperador mogol',['Akbar','Jahangir','Shah Jahan','Aurangzeb']),
 ('HIST-Q83618','Chhatrapati · soberano maratha',['Shivaji','Sambhaji','Rajaram I']),
 ('AYUTTHAYA','Rey de Ayutthaya',['Naresuan','Ekathotsarot','Si Saowaphak','Songtham','Chetthathirat','Athittayawong','Prasat Thong','Chai (king of Ayutthaya)','Si Suthammaracha','Narai','Phetracha']),
 ('DENMARK-NORWAY','Rey de Dinamarca y Noruega',['Christian IV of Denmark','Frederick III of Denmark','Christian V of Denmark']),
 ('SWE','Rey / reina de Suecia',['Charles IX of Sweden','Gustavus Adolphus','Christina, Queen of Sweden','Charles X Gustav','Charles XI of Sweden','Charles XII of Sweden']),
 ('POLISH-LITHUANIAN','Rey de Polonia y gran duque de Lituania',['Sigismund III Vasa','Władysław IV Vasa','John II Casimir Vasa','Michael I of Poland','John III Sobieski','Augustus II the Strong'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index("if __name__")].replace('core019-rulers.json','rulers020-candidates.json').replace('core019meta-','rulers020meta-');exec(compile(code,'rulers020','exec'),r.__dict__)
if __name__=='__main__':r.main()
