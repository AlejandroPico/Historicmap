"""Additional named sixteenth-century office research; no public data writes."""
import pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('r',ROOT/'scripts/review-019-core-rulers.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
r.GROUPS=[
 ('PAPAL-STATES','Papa · soberano temporal',['Pope Alexander VI','Pope Pius III','Pope Julius II','Pope Leo X','Pope Adrian VI','Pope Clement VII','Pope Paul III','Pope Julius III','Pope Marcellus II','Pope Paul IV','Pope Pius IV','Pope Pius V','Pope Gregory XIII','Pope Sixtus V','Pope Urban VII','Pope Gregory XIV','Pope Innocent IX','Pope Clement VIII']),
 ('DENMARK-NORWAY','Rey de Dinamarca y Noruega',['John, King of Denmark','Christian II of Denmark','Frederick I of Denmark','Christian III of Denmark','Frederick II of Denmark','Christian IV of Denmark']),
 ('POLAND-KINGDOM','Rey de Polonia',['John I Albert','Alexander Jagiellon','Sigismund I the Old','Sigismund II Augustus']),
 ('SAADI','Sultán saadí',['Mohammed al-Shaykh','Abdallah al-Ghalib','Abu Abdallah Mohammed II Saadi','Abu Marwan Abd al-Malik I','Ahmad al-Mansur']),
 ('WATTASID','Sultán wattasí',['Abu Abd Allah al-Sheikh Muhammad ibn Yahya','Abu Abd Allah al-Burtuqali Muhammad ibn Muhammad','Abu al-Abbas Ahmad ibn Muhammad']),
 ('MAMLUKS','Sultán mameluco',['Qansuh al-Ghawri','Tuman bay II']),
 ('LODI','Sultán de Delhi',['Sikandar Lodi','Ibrahim Lodi']),
 ('HIST-Q167639','Soberano de Vijayanagara',['Krishnadevaraya','Achyuta Deva Raya','Sadashiva Raya']),
 ('AYUTTHAYA','Rey de Ayutthaya',['Maha Chakkraphat','Maha Thammaracha','Naresuan']),
 ('EAST-HUNGARY','Rey de Hungría oriental',['John Zápolya','John Sigismund Zápolya']),
 ('FLORENCE-DUCHY','Duque de Florencia',['Alessandro de Medici','Cosimo I de Medici']),
 ('HIST-Q4948','Dux de Venecia',['Agostino Barbarigo','Leonardo Loredan','Antonio Grimani','Andrea Gritti','Pietro Lando','Francesco Donà','Marcantonio Trevisan','Francesco Venier','Lorenzo Priuli','Girolamo Priuli','Pietro Loredan','Alvise I Mocenigo','Sebastiano Venier','Nicolò da Ponte','Pasquale Cicogna','Marino Grimani']),
 ('SAVOY-DUCHY','Duque de Saboya',['Philibert II, Duke of Savoy','Charles III, Duke of Savoy','Emmanuel Philibert, Duke of Savoy'])]
code=(ROOT/'scripts/review-019-core-rulers.py').read_text(encoding='utf8');code=code[code.index('def main():'):code.index('if __name__')].replace('core019-rulers.json','rulers021-additional.json').replace('core019meta-','rulers021additional-');exec(compile(code,'additional021','exec'),r.__dict__)
if __name__=='__main__':r.main()
