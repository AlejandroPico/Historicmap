"""Rebuild the small, reviewed country-history catalogue without network requests.

Original Spanish summaries of the linked institutional sources. This catalogue is
an editorial navigation index, not a complete database of international succession.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = "2026-10-23"
SOURCES = {
    "ussr": ("https://1997-2001.state.gov/background_notes/russia_0898_bgn.html", "Departamento de Estado de EE. UU. · Rusia, antecedentes de 1998"),
    "un-russia": ("https://www.un.org/en/about-us/member-states/russian-federation", "ONU · Federación de Rusia"),
    "treaties": ("https://treaties.un.org/pages/HistoricalInfo.aspx", "ONU · Información histórica del depositario de tratados"),
    "estonia": ("https://vm.ee/en/news/foreign-minister-margus-tsahkna-35-years-restoration-independence-reminds-us-freedom-value", "Ministerio de Exteriores de Estonia · Restauración de la independencia"),
    "latvia": ("https://www.mfa.gov.lv/lv/arlietu-ministrijas-darbibas-atjaunosana-1990-1991", "Ministerio de Exteriores de Letonia · Restauración 1990–1991"),
    "lithuania": ("https://www.lrs.lt/sip/portal.show?p_k=2&p_r=35660", "Parlamento de Lituania · Acto del 11 de marzo de 1990"),
    "un-yugoslavia": ("https://www.un.org/en/about-us/member-states/yugoslavia", "ONU · Yugoslavia y Estados sucesores"),
    "yugoslavia-treaties": ("https://digitallibrary.un.org/record/558855/files/A_60_351-EN.pdf", "ONU · Sucesión en tratados, A/60/351"),
    "fry": ("https://digitallibrary.un.org/record/142149?ln=en", "ONU · Declaración del 27 de abril de 1992, S/23877"),
    "czechoslovakia": ("https://www.un.org/en/about-us/member-states/czechoslovakia", "ONU · Checoslovaquia y Estados sucesores"),
    "germany": ("https://www.bundesregierung.de/breg-de/schwerpunkte/deutsche-einheit/einigungsvertrag-353990", "Gobierno federal alemán · Tratado de unificación"),
    "yemen": ("https://www.un.org/en/about-us/growth-in-un-membership", "ONU · Evolución de la membresía, unificación de Yemen"),
    "south-sudan": ("https://unterm.un.org/unterm2/en/view/UNHQ/dd08eda8-c78a-4f4f-bd1f-8c2d1538e03d", "ONU · Independencia y admisión de Sudán del Sur"),
    "eritrea": ("https://digitallibrary.un.org/record/218378?ln=en", "ONU · Mensaje del 24 de mayo de 1993 sobre Eritrea"),
    "eritrea-referendum": ("https://digitallibrary.un.org/record/173272/files/327786-EN.pdf", "ONU · Informe anual de 1993, referéndum de Eritrea"),
    "timor": ("https://peacekeeping.un.org/sites/default/files/past/etimor/etimor.htm", "ONU · Administración transitoria de Timor Oriental, UNTAET"),
    "namibia": ("https://peacekeeping.un.org/sites/default/files/past/untagFT.htm", "ONU · Grupo de asistencia a la transición de Namibia, UNTAG"),
    "kosovo": ("https://www.icj-cij.org/node/103912", "Corte Internacional de Justicia · Resumen de la opinión consultiva de 2010"),
    "spain": ("https://www.boe.es/diario_boe/txt.php?id=BOE-A-1978-31229&lang=es", "BOE · Constitución Española de 1978"),
    "spain-1931": ("https://www.cultura.gob.es/cultura/areas/archivos/mc/archivos/cdmh/exposiciones-y-actividades/echa-un-vistazo/constitucion-1931.html", "Ministerio de Cultura · Constitución de 1931"),
    "spain-1975": ("https://www.congreso.es/eu/cem/proclamacion-rey-juan-carlos", "Congreso de los Diputados · Proclamación de Juan Carlos I"),
    "france": ("https://qpc360.conseil-constitutionnel.fr/constitution-4-octobre-1958", "Consejo Constitucional de Francia · Constitución de 1958"),
    "france-promulgation": ("https://www.senat.fr/reglement/pouvoirs_publics4.html", "Senado de Francia · Promulgación de la Constitución de 1958"),
    "germany-law": ("https://www.gesetze-im-internet.de/englisch_gg/englisch_gg.html", "Ministerio de Justicia alemán · Ley Fundamental"),
    "japan": ("https://www.shugiin.go.jp/internet/itdb_english.nsf/html/statics/english/constitution_e.htm", "Cámara de Representantes de Japón · Constitución"),
    "india": ("https://sansad.in/ls/about/introduction", "Parlamento de India · Constitución y organización parlamentaria"),
    "brazil": ("https://www4.planalto.gov.br/legislacao/legis-federal/constituicao", "Presidencia de Brasil · Constitución de 1988"),
    "brazil-date": ("https://www.planalto.gov.br/ccivil_03/constituicao/douconstituicao88.pdf", "Diario Oficial de Brasil · Constitución del 5 de octubre de 1988"),
    "south-africa": ("https://www.justice.gov.za/constitution/SAConstitution-web-eng.pdf", "Ministerio de Justicia de Sudáfrica · Constitución de 1996"),
    "italy": ("https://www.senato.it/documenti/repository/istituzione/costituzione_inglese.pdf", "Senado de Italia · Constitución"),
    "portugal": ("https://www.parlamento.pt/legislacao/documents/constitution7threv2010en.pdf", "Asamblea de la República de Portugal · Constitución"),
    "switzerland": ("https://www.parlament.ch/en/%C3%BCber-das-parlament/Pages/bundesverfassung.aspx", "Parlamento de Suiza · Historia de la Constitución federal"),
    "usa": ("https://www.archives.gov/founding-docs/constitution/what-does-it-say", "Archivos Nacionales de EE. UU. · Organización constitucional"),
    "canada": ("https://www.ourcommons.ca/procedure-and-practice-4/ch01-3-e.html", "Cámara de los Comunes de Canadá · Sistema de gobierno"),
    "mexico": ("https://ordenjuridico.gob.mx/Documentos/Federal/html/wo14166.html", "Gobierno de México · Constitución de 1917"),
    "argentina": ("https://www.congreso.gob.ar/constitucionParte1Cap1.php", "Congreso de Argentina · Constitución Nacional"),
}

relations = []
records = []


def relation(id, from_key, from_name, from_year, to_key, to_name, to_year,
             date, kind, label, note, source):
    url, source_label = SOURCES[source]
    relations.append({"id": id, "from": {"key": from_key, "name": from_name, "year": from_year},
                      "to": {"key": to_key, "name": to_name, "year": to_year},
                      "date": date, "type": kind, "label": label, "note": note,
                      "source": url, "sourceLabel": source_label})


def record(id, keys, start, section, title, text, source, end=None, **extra):
    url, source_label = SOURCES[source]
    item = {"id": id, "keys": keys, "start": start, "section": section,
            "title": title, "text": text, "source": url, "sourceLabel": source_label, **extra}
    if end:
        item["end"] = end
    records.append(item)


# The date on these links is the end of the union, not each declaration date.
for key, name in [("ARM", "Armenia"), ("AZE", "Azerbaiyán"), ("BLR", "Bielorrusia"),
                  ("GEO", "Georgia"), ("KAZ", "Kazajistán"), ("KGZ", "Kirguistán"),
                  ("MDA", "Moldavia"), ("TJK", "Tayikistán"), ("TKM", "Turkmenistán"),
                  ("UKR", "Ucrania"), ("UZB", "Uzbekistán")]:
    relation(f"ussr-{key.lower()}", "USSR", "Unión Soviética", 1990, key, name, 1992,
             "1991-12-26", "dissolution", f"Disolución de la URSS → {name}",
             "Fecha de disolución; no de la declaración de independencia.", "ussr")

relation("ussr-russia", "USSR", "Unión Soviética", 1990, "RUS", "Federación de Rusia", 1992,
         "1991-12-24", "continuation", "Continuidad de la membresía soviética en la ONU",
         "La comunicación rusa a la ONU no convierte a Rusia en único sucesor territorial de la URSS.", "un-russia")
for key, name, date, source in [("EST", "Estonia", "1991-08-20", "estonia"),
                               ("LVA", "Letonia", "1991-08-21", "latvia"),
                               ("LTU", "Lituania", "1990-03-11", "lithuania")]:
    relation(f"ussr-{key.lower()}", "USSR", "Unión Soviética", 1990, key, name, 1992,
             date, "restoration", f"Restauración de la independencia de {name}",
             "Se distingue restauración estatal de sucesión automática; el año de navegación muestra una entidad cartográfica disponible.", source)

# Treaty-effective succession dates are distinguished from other independence milestones.
for key, name, date, year in [("SVN", "Eslovenia", "1991-06-25", 1992),
                             ("HRV", "Croacia", "1991-10-08", 1992),
                             ("BIH", "Bosnia y Herzegovina", "1992-03-06", 1993),
                             ("MKD", "Macedonia", "1991-09-17", 1993)]:
    relation(f"yug-{key.lower()}", "YUG", "Yugoslavia socialista", 1990, key, name, year,
             date, "dissolution", f"Desintegración yugoslava → {name}",
             "Fecha efectiva de sucesión en tratados recogida por la ONU; no equivale a todos los hitos de independencia o reconocimiento.", "yugoslavia-treaties")
relation("yug-fry", "YUG", "Yugoslavia socialista", 1990, "FRY", "República Federal de Yugoslavia", 1993,
         "1992-04-27", "dissolution", "Formación de la federación de Serbia y Montenegro",
         "Nueva federación de dos repúblicas. La pretensión inicial de continuidad no fue continuidad automática de la membresía ONU.", "fry")
relation("fry-scg", "FRY", "República Federal de Yugoslavia", 2002, "SCG", "Serbia y Montenegro", 2003,
         "2003-02-04", "reconstitution", "Unión estatal de Serbia y Montenegro",
         "Cambio de denominación y marco constitucional; no nueva admisión en la ONU.", "un-yugoslavia")
relation("scg-srb", "SCG", "Serbia y Montenegro", 2005, "SRB", "Serbia", 2006,
         "2006-06-03", "continuation", "Serbia continúa la membresía de la unión estatal",
         "Continuidad comunicada a la ONU tras la independencia montenegrina.", "treaties")
relation("scg-mne", "SCG", "Serbia y Montenegro", 2005, "MNE", "Montenegro", 2006,
         "2006-06-03", "independence", "Independencia de Montenegro",
         "Admisión separada en la ONU el 28 de junio de 2006.", "un-yugoslavia")
for key, name in [("CZE", "Chequia"), ("SVK", "Eslovaquia")]:
    relation(f"csk-{key.lower()}", "CSK", "Checoslovaquia", 1992, key, name, 1993,
             "1993-01-01", "dissolution", f"Separación checoslovaca → {name}",
             "Checoslovaquia dejó de existir al terminar 1992; ambos Estados ingresaron por separado en la ONU el 19 de enero de 1993.", "czechoslovakia")
relation("ddr-deu", "DDR", "República Democrática Alemana", 1989, "DEU", "Alemania reunificada", 1990,
         "1990-10-03", "accession", "Reunificación alemana",
         "Adhesión de la RDA a la República Federal; no fusión de dos Estados para crear una nueva RDA.", "germany")
for key, name in [("YAR", "República Árabe de Yemen"), ("YPR", "República Democrática Popular del Yemen")]:
    relation(f"{key.lower()}-yem", key, name, 1989, "YEM", "República de Yemen", 1990,
             "1990-05-22", "unification", "Unificación de Yemen",
             "Los dos miembros de Naciones Unidas quedaron representados como un solo Yemen.", "yemen")
relation("sdn-sds", "SDN", "Sudán antes de la separación", 2010, "SDS", "Sudán del Sur", 2011,
         "2011-07-09", "independence", "Independencia de Sudán del Sur",
         "La separación no extingue Sudán. Admisión del nuevo Estado en la ONU el 14 de julio.", "south-sudan")
relation("eth-eri", "ETH", "Etiopía antes de la independencia eritrea", 1990, "ERI", "Eritrea", 1993,
         "1993-05-24", "independence", "Independencia de Eritrea",
         "Fecha de las celebraciones oficiales de independencia, posterior al referéndum y a su declaración de abril; Etiopía continúa existiendo.", "eritrea")
relation("idn-tls", "IDN", "Indonesia durante la ocupación de Timor Oriental", 1998, "TLS", "Timor-Leste", 2002,
         "2002-05-20", "independence", "Independencia de Timor-Leste",
         "Entre la ocupación indonesia y la independencia medió UNTAET (1999–2002). El enlace no reconoce la anexión indonesia ni una independencia de Indonesia aceptada por la ONU.", "timor")
relation("zaf-nam", "ZAF", "Sudáfrica durante la administración de Namibia", 1989, "NAM", "Namibia", 1990,
         "1990-03-21", "decolonization", "Independencia de Namibia",
         "Final de la administración sudafricana mediante el proceso supervisado por la ONU; no reconocimiento de soberanía sudafricana sobre Namibia.", "namibia")
relation("srb-kos", "SRB", "Serbia", 2007, "KOS", "Kosovo", 2008,
         "2008-02-17", "declaration", "Declaración de independencia de Kosovo",
         "Reconocimiento internacional dividido. La opinión de la CIJ de 2010 sobre la declaración no decidió de forma general la estatalidad ni obligó a reconocerla.", "kosovo")

# Institutional summaries describe stable constitutional features, not a full
# version history of every amendment or a ranking of democratic practice.
institutional = [
    ("esp-constitution", ["ESP"], "1978-12-29", "Monarquía parlamentaria", "La Constitución de 1978 establece una monarquía parlamentaria. La Corona ocupa la jefatura del Estado; el Gobierno responde ante el Congreso. El poder legislativo corresponde a las Cortes Generales, con Congreso y Senado.", "spain"),
    ("fra-fifth-republic", ["FRA"], "1958-10-04", "Quinta República", "Marco constitucional con Presidencia de la República y Gobierno dirigido por un primer ministro. El Gobierno determina y conduce la política nacional y responde ante el Parlamento; este reúne Asamblea Nacional y Senado. Las reglas concretas han recibido reformas.", "france"),
    ("deu-basic-law", ["DEU"], "1949-05-24", "República federal y Gobierno parlamentario", "La Ley Fundamental organiza una federación. El Bundestag elige al canciller federal; la Presidencia federal y la Cancillería son cargos distintos. Los Länder participan en la legislación federal a través del Bundesrat. En 1990 su ámbito se amplió con la reunificación.", "germany-law"),
    ("jpn-constitution", ["JPN"], "1947-05-03", "Emperador y gabinete parlamentario", "El emperador simboliza el Estado y carece de poderes de gobierno. La Dieta designa al primer ministro y el gabinete responde colectivamente ante ella. Se distinguen las funciones simbólicas de la Corona del ejercicio del poder ejecutivo.", "japan"),
    ("ind-constitution", ["IND"], "1950-01-26", "República federal parlamentaria", "La Constitución establece una organización federal y parlamentaria. El Parlamento de la Unión comprende la Presidencia, Rajya Sabha y Lok Sabha. El Gobierno es colectivamente responsable ante la Lok Sabha; Presidencia y jefatura del Gobierno son distintas.", "india"),
    ("bra-constitution", ["BRA"], "1988-10-05", "República federativa presidencial", "La Constitución de 1988 organiza la Unión, los estados, el Distrito Federal y los municipios. La Presidencia encabeza el ejecutivo y el Congreso Nacional comprende Cámara de Diputados y Senado Federal. No se trasladan al pasado las reglas de duración de mandatos de reformas posteriores.", "brazil"),
    ("zaf-constitution", ["ZAF"], "1997-02-04", "Marco constitucional de 1996", "La Constitución de 1996 entra en vigor, con las excepciones previstas en ella, el 4 de febrero de 1997. La Asamblea Nacional elige al presidente, que es jefe del Estado y del ejecutivo nacional. El Parlamento comprende Asamblea Nacional y Consejo Nacional de Provincias.", "south-africa"),
    ("ita-constitution", ["ITA"], "1948-01-01", "República parlamentaria", "La Constitución republicana entra en vigor el 1 de enero de 1948. Distingue Presidencia de la República y Gobierno; este necesita la confianza de las cámaras. El Parlamento incluye Cámara de Diputados y Senado de la República.", "italy"),
    ("prt-constitution", ["PRT"], "1976-04-25", "República constitucional", "La Constitución de 1976 organiza Presidencia, Asamblea de la República, Gobierno y tribunales como órganos de soberanía. El Gobierno está políticamente vinculado a la Presidencia y a la Asamblea. La ficha resume esta estructura sin tratar todas las revisiones como un mismo texto inmutable.", "portugal"),
    ("che-constitution", ["CHE"], "2000-01-01", "Constitución federal de 1999", "La revisión total aprobada por el pueblo y los cantones en 1999 entra en vigor el 1 de enero de 2000 y sustituye el texto de 1874. Conserva la estructura federal y los mecanismos de iniciativa y referéndum. Su aprobación no equivale a la fundación del Estado suizo.", "switzerland"),
    ("usa-constitution", ["USA"], "1990-01-01", "Presidencia, Congreso y justicia federal", "La Constitución distribuye el poder federal entre el Congreso bicameral, la Presidencia y los tribunales. Los controles recíprocos y las competencias de los estados forman parte de esta estructura. El inicio de 1990 delimita la cobertura de esta síntesis, no la fecha de fundación de las instituciones.", "usa"),
    ("can-constitution", ["CAN"], "1990-01-01", "Monarquía constitucional y federación", "La Corona, el Senado y la Cámara de los Comunes integran el Parlamento. El Gobierno depende de la confianza de los Comunes y la federación distribuye competencias entre el nivel federal y las provincias. El marco incluye las leyes constitucionales de 1867 y 1982; 1990 es el inicio editorial de cobertura.", "canada"),
    ("mex-constitution", ["MEX"], "1990-01-01", "República representativa y federal", "La Constitución de 1917 organiza la república federal y separa los poderes legislativo, ejecutivo y judicial. El Congreso comprende Cámara de Diputados y Senado; la Presidencia encabeza el ejecutivo. La síntesis se aplica desde 1990 y no certifica las mismas reglas electorales para todo el siglo XX.", "mexico"),
    ("arg-constitution", ["ARG"], "1995-01-01", "República representativa y federal", "La Constitución define una forma representativa, republicana y federal. El Congreso es bicameral y distingue competencias nacionales y provinciales. El inicio de 1995 es un límite editorial posterior a la reforma de 1994; no es la fecha de creación de la república ni de su Constitución original.", "argentina"),
]
for id, keys, start, title, text, source in institutional:
    record(id, keys, start, "institutions", title, text, source)

# One-day intervals describe events. They do not remain active institutional rules.
events = [
    ("esp-republic-1931", ["ESP", "ESP-REPUBLIC"], "1931-04-14", "Segunda República", "La proclamación de la Segunda República abre el proceso constituyente de 1931.", "spain-1931"),
    ("esp-constitution-1931", ["ESP", "ESP-REPUBLIC"], "1931-12-09", "Constitución republicana de 1931", "Las Cortes aprueban la Constitución de la Segunda República. Este hito no afirma que su aplicación fuese uniforme durante la guerra civil.", "spain-1931"),
    ("esp-crown-1975", ["ESP"], "1975-11-22", "Proclamación de Juan Carlos I", "Juan Carlos I es proclamado rey ante las Cortes. La proclamación y la posterior Constitución parlamentaria de 1978 son hitos distintos.", "spain-1975"),
    ("esp-constitution-1978", ["ESP"], "1978-12-29", "Entrada en vigor de la Constitución", "La publicación de la Constitución en el BOE marca su entrada en vigor. El referéndum había tenido lugar el 6 de diciembre y la sanción el 27.", "spain"),
    ("fra-constitution-1958", ["FRA"], "1958-10-04", "Constitución de la Quinta República", "Se promulga la Constitución de 1958, después del referéndum del 28 de septiembre; se publica al día siguiente.", "france-promulgation"),
    ("bra-constitution-1988", ["BRA"], "1988-10-05", "Constitución de 1988", "Se promulga la Constitución brasileña de 1988, nuevo marco de la república federativa tras la transición civil.", "brazil-date"),
    ("zaf-constitution-1997", ["ZAF"], "1997-02-04", "Nueva Constitución en vigor", "Entra en vigor el marco constitucional definitivo de 1996, salvo las excepciones indicadas por sus disposiciones de aplicación.", "south-africa"),
    ("che-constitution-2000", ["CHE"], "2000-01-01", "Revisión total constitucional", "Entra en vigor el texto constitucional aprobado en 1999 y se sustituye la Constitución de 1874.", "switzerland"),
    ("fry-admission-2000", ["FRY"], "2000-11-01", "Admisión de la Yugoslavia federal en la ONU", "La República Federal de Yugoslavia es admitida como miembro de Naciones Unidas; no se retrotrae esta admisión a 1992.", "un-yugoslavia"),
    ("tls-untaet-1999", ["TLS", "IDN"], "1999-10-25", "Administración transitoria en Timor Oriental", "Se establece UNTAET para administrar el territorio y ejercer autoridad legislativa y ejecutiva durante la transición. Es una fase anterior a la independencia de 2002.", "timor"),
    ("eri-referendum-1993", ["ERI", "ETH"], "1993-04-23", "Referéndum de Eritrea", "La votación del 23 al 25 de abril es verificada por la ONU. Le siguen la declaración de abril y las celebraciones oficiales de independencia de mayo, fechas que no deben confundirse.", "eritrea-referendum"),
    ("kos-opinion-2010", ["KOS", "SRB"], "2010-07-22", "Opinión consultiva de la CIJ", "La Corte concluye que la declaración de 2008 no vulneró el derecho internacional. Su respuesta no decide de manera general la estatalidad de Kosovo ni obliga al reconocimiento.", "kosovo"),
]
from datetime import date, timedelta
for id, keys, start, title, text, source in events:
    finish = "1993-04-26" if id == "eri-referendum-1993" else (date.fromisoformat(start) + timedelta(days=1)).isoformat()
    record(id, keys, start, "history", title, text, source, end=finish)

record("sdn-after-2011", ["SDN", "SDS"], "2011-07-09", "territory", "Separación de Sudán del Sur", "Sudán del Sur se constituye como Estado separado; Sudán continúa existiendo. Las estadísticas anteriores de todo Sudán no se reparten automáticamente entre ambos, y el hito no resuelve por sí solo los límites disputados.", "south-sudan")
record("tls-transition", ["TLS"], "1999-10-25", "institutions", "Administración transitoria de Naciones Unidas", "UNTAET ejerce funciones legislativas y ejecutivas en Timor Oriental durante la transición hacia el autogobierno. El 20 de mayo de 2002 se transfieren las funciones a las instituciones independientes.", "timor", end="2002-05-20")

# Reviewed 1970–1989 extension. Navigation anchors are not assertions that a
# colonial administrator was the same entity as the territory becoming independent.
SOURCES.update({
    "vietnam-union": ("https://treaties-prod.un.org/pages/HistoricalInfo.aspx?clang=_en", "ONU · Depositario de tratados, unificación vietnamita"),
    "bangladesh-1971": ("https://history.state.gov/milestones/1969-1976/south-asia", "Departamento de Estado · Crisis surasiática de 1971"),
    "guinea-1973": ("https://documents.un.org/doc/undoc/gen/n09/387/22/pdf/n0938722.pdf", "Guinea-Bissau · Informe estatal CEDAW/C/GNB/6 ante la ONU"),
    "portugal-democracy": ("https://www.parlamento.pt/Parlamento/Paginas/democracia.aspx", "Asamblea de Portugal · Estado democrático"),
    "greece-history": ("https://www.hellenicparliament.gr/en/vouli-ton-ellinon/to-politevma/syntagmatiki-istoria/", "Parlamento heleno · Historia constitucional"),
    "greece-law": ("https://www.hellenicparliament.gr/userfiles/f3c70a23-7696-49db-9148-f24dce6a27c8/001-156%20aggliko.pdf", "Parlamento heleno · Constitución y evolución de 1975/1986"),
    "spain-elections": ("https://constitucion.congreso.es/constitucion-1978/elaboracion/cortesconstituyentes", "Congreso de España · Elecciones y Cortes constituyentes"),
    "argentina-democracy": ("https://www.argentina.gob.ar/node/411931", "Gobierno argentino · Dictadura y recuperación democrática"),
    "canada-1982": ("https://laws.justice.gc.ca/eng/const/FullText.html", "Ministerio de Justicia de Canadá · Leyes constitucionales de 1867–1982"),
    "chile-vote": ("https://www.bcn.cl/historiapolitica/elecciones/index.html?periodo=1973-1990", "Biblioteca del Congreso de Chile · Elecciones, 1973–1990"),
    "poland-roundtable": ("https://www.president.pl/archives/bronislaw-komorowski/freedom-day/1989", "Presidencia de Polonia · Cambios institucionales de 1989"),
    "czechoslovakia-1989": ("https://mzv.gov.cz/copenhagen/en/news/x2015/twenty_six_years_since_the_velvet.mobi", "Ministerio de Exteriores checo · Revolución de Terciopelo"),
    "berlin-1989": ("https://www.bundestag.de/dokumente/textarchiv/1989-11-09-mauerfall-337756", "Bundestag · Apertura del Muro de Berlín"),
})
for slug, label in [("angola", "Angola"), ("mozambique", "Mozambique"), ("sao-tome-and-principe", "Santo Tomé y Príncipe"),
                    ("djibouti", "Yibuti"), ("papua-new-guinea", "Papúa Nueva Guinea"), ("solomon-islands", "Islas Salomón"),
                    ("vanuatu", "Vanuatu"), ("zimbabwe", "Zimbabue"), ("suriname", "Surinam")]:
    SOURCES[f"decolonization-{slug}"] = (f"https://history.state.gov/countries/{slug}", f"Departamento de Estado · Independencia y reconocimiento de {label}")

relation("vdr-vnm", "VDR", "República Democrática de Vietnam", 1974, "VNM", "Vietnam unificado", 1976,
         "1976-07-02", "unification", "Constitución del Vietnam unificado",
         "La unificación formal de 1976 se distingue del control militar de 1975. No se heredan automáticamente estadísticas de un sucesor.", "vietnam-union")
relation("rvn-vnm", "RVN", "República de Vietnam", 1974, "VNM", "Vietnam unificado", 1976,
         "1976-07-02", "unification", "Del Vietnam del Sur al Estado unificado",
         "Entre la caída de la República de Vietnam en abril de 1975 y la unificación formal existió la República de Vietnam del Sur. La base CShapes agrupa el control de 1975 bajo el Norte y no ofrece una entidad provisional separada navegable.", "vietnam-union")
record("vnm-unification-1976", ["VDR", "RVN", "VSR", "VNM"], "1976-07-02", "history", "Unificación formal vietnamita",
       "Vietnam del Norte y la República de Vietnam del Sur se unen como República Socialista de Vietnam. El cambio institucional no equivale a una frontera diaria o a heredar las estadísticas de las entidades anteriores.", "vietnam-union", end="1976-07-03")
relation("pak-bgd", "PAK", "Pakistán antes de la separación oriental", 1970, "BGD", "Bangladesh", 1972,
         "1971-12-16", "independence", "Separación de Bangladesh",
         "La fecha corresponde a la rendición de diciembre y al final de la guerra de ese año, no a la proclamación de marzo ni a la admisión ONU de 1974. Pakistán continúa existiendo.", "bangladesh-1971")

decolonization = [
    ("PRT", "Portugal", 1970, "AGO", "Angola", "1975-11-11", "angola", "La independencia no significa fin inmediato de la guerra civil."),
    ("PRT", "Portugal", 1970, "MOZ", "Mozambique", "1975-06-25", "mozambique", "Fecha de independencia y reconocimiento estadounidense; no cierra los conflictos posteriores."),
    ("PRT", "Portugal", 1970, "STP", "Santo Tomé y Príncipe", "1975-07-12", "sao-tome-and-principe", "Fecha de independencia, distinguida del establecimiento de relaciones diplomáticas."),
    ("FRA", "Francia", 1970, "DJI", "Yibuti", "1977-06-27", "djibouti", "El territorio antes administrado por Francia se constituye como Estado independiente."),
    ("AUS", "Australia", 1970, "PNG", "Papúa Nueva Guinea", "1975-09-16", "papua-new-guinea", "Final de la administración australiana, con territorios de distinta procedencia jurídica."),
    ("GBR", "Reino Unido", 1970, "SLB", "Islas Salomón", "1978-07-07", "solomon-islands", "Se distingue independencia de establecimiento posterior de relaciones diplomáticas."),
    ("GBR", "Reino Unido", 1970, "VUT", "Vanuatu", "1980-07-30", "vanuatu", "Final del condominio anglo-francés; el enlace británico se complementa con el francés."),
    ("FRA", "Francia", 1970, "VUT", "Vanuatu", "1980-07-30", "vanuatu", "Final del condominio anglo-francés; no dos independencias o dos territorios separados."),
    ("GBR", "Reino Unido", 1970, "ZWE", "Zimbabue", "1980-04-18", "zimbabwe", "Se distingue del régimen rodesiano de independencia unilateral no reconocida de 1965."),
    ("NLD", "Países Bajos", 1970, "SUR", "Surinam", "1975-11-25", "suriname", "Independencia tras una etapa previa de autonomía; no fecha de fundación de todos sus órganos."),
]
for administrator, administrator_name, anchor, key, name, day, source, note in decolonization:
    relation(f"decolonization-{administrator.lower()}-{key.lower()}", administrator, administrator_name, anchor,
             key, name, int(day[:4]), day, "decolonization", f"Descolonización → {name}",
             f"Enlace de la potencia administradora al territorio independiente; no identidad estatal compartida. {note}", f"decolonization-{source}")
    # The two Vanuatu administrator links share a single independent-state event.
    if key != "VUT" or administrator == "GBR":
        record(f"{key.lower()}-independence-{day[:4]}", [key], day, "history", f"Independencia de {name}",
               note, f"decolonization-{source}", end=(date.fromisoformat(day)+timedelta(days=1)).isoformat())
relation("prt-gnb", "PRT", "Portugal", 1970, "GNB", "Guinea-Bissau", 1974,
         "1973-09-24", "declaration", "Proclamación de independencia de Guinea-Bissau",
         "Proclamación del PAIGC en 1973; reconocimiento portugués en 1974. La navegación usa un año con entidad independiente en la fuente.", "guinea-1973")
relation("prt-cpv", "PRT", "Portugal", 1970, "CPV", "Cabo Verde", 1975,
         "1975-07-05", "decolonization", "Independencia de Cabo Verde",
         "Independencia negociada, separada de la proclamación guineana de 1973.", "guinea-1973")

# These are dated institutional phases. Present-day consolidated law must not be
# retrojected to a dictatorship or to the other German/Vietnamese state.
record("prt-revolutionary-transition", ["PRT"], "1974-04-25", "institutions", "Instituciones provisionales de la transición",
       "El derribo de la dictadura abre una transición con órganos y gobiernos provisionales. Se prepara un nuevo orden democrático; esta fase no equivale todavía a una constitución parlamentaria en vigor.", "portugal-democracy", end="1975-04-25")
record("prt-constituent-institutions", ["PRT"], "1975-04-25", "institutions", "Asamblea Constituyente y gobiernos de transición",
       "Las elecciones de abril de 1975 dan lugar a una Asamblea Constituyente que elabora el nuevo marco institucional. Los gobiernos provisionales continúan durante esta fase; la aprobación y entrada en vigor constitucional son hitos distintos.", "portugal-democracy", end="1976-04-25")
record("grc-republic-1975", ["GRC"], "1975-06-11", "institutions", "República parlamentaria constitucional",
       "El marco de 1975 establece la república parlamentaria tras la dictadura y el referéndum de 1974. Esta síntesis describe la estructura general, sin atribuirle todas las versiones posteriores del articulado.", "greece-law")
record("grc-revision-1986", ["GRC"], "1986-03-06", "history", "Resolución de revisión constitucional de 1986",
       "El Parlamento adopta la resolución de revisión constitucional de marzo de 1986. Cambia el equilibrio entre Presidencia y Gobierno dentro del marco republicano, sin crear por primera vez la república de 1975.", "greece-law", end="1986-03-07")
record("esp-constituent-1977", ["ESP"], "1977-06-15", "institutions", "Elecciones y Cortes constituyentes",
       "Las elecciones del 15 de junio dan lugar a unas Cortes plurales que elaboran el nuevo marco constitucional. Congreso y Senado inician su actividad en julio; no se aplica todavía la Constitución de 1978.", "spain-elections", end="1978-12-29")
record("can-charter-1982", ["CAN"], "1982-04-17", "history", "Ley constitucional de 1982",
       "La Ley constitucional de 1982 incorpora la Carta de Derechos y Libertades y un procedimiento de reforma. El hito modifica el marco constitucional, sin crear por primera vez la federación canadiense.", "canada-1982", end="1982-04-18")
record("arg-return-1983", ["ARG"], "1983-12-10", "history", "Recuperación de las instituciones democráticas",
       "La asunción de autoridades constitucionales cierra la dictadura iniciada en marzo de 1976. Este registro no traslada al año 1983 las reformas constitucionales de 1994.", "argentina-democracy", end="1983-12-11")
record("chl-plebiscite-1988", ["CHL"], "1988-10-05", "history", "Plebiscito de 1988",
       "La opción No rechaza la prolongación de Pinochet en la presidencia. Se abre un proceso electoral de transición; la transferencia presidencial no se produce ese mismo día.", "chile-vote", end="1988-10-06")
record("pol-roundtable-1989", ["POL"], "1989-02-06", "history", "Apertura de la mesa redonda",
       "Gobierno y oposición inician negociaciones sobre la apertura del sistema político. El comienzo del diálogo no se confunde con la posterior votación o la toma de posesión de un nuevo gobierno.", "poland-roundtable", end="1989-02-07")
record("ddr-wall-1989", ["DDR", "DEU"], "1989-11-09", "history", "Apertura del Muro de Berlín",
       "La apertura de los pasos permite circular entre ambos lados. Los dos Estados alemanes aún no se han reunificado; la adhesión de la RDA se produce en otro año.", "berlin-1989", end="1989-11-10")
record("csk-velvet-1989", ["CSK"], "1989-11-17", "history", "Movilización de la Revolución de Terciopelo",
       "La represión de una manifestación estudiantil abre una oleada de protestas y huelgas. El proceso transforma las instituciones de Checoslovaquia, sin separarla todavía en dos Estados.", "czechoslovakia-1989", end="1989-11-18")

# Extend only stable summaries whose wording does not import later amendments.
for item in records:
    if item["id"] == "usa-constitution":
        item["start"]="1970-01-01"
        item["text"]=item["text"].replace("1990", "1970")
    if item["id"] == "mex-constitution":
        item["start"]="1970-01-01"
        item["text"]=item["text"].replace("1990", "1970")
relation("rvn-vsr", "RVN", "República de Vietnam", 1974, "VSR", "República de Vietnam del Sur · Gobierno Revolucionario Provisional", 1975,
         "1975-04-30", "regime-change", "Fin del Gobierno de Saigón y administración revolucionaria sureña",
         "El Gobierno Revolucionario Provisional existía desde 1969 como autoridad rival. El enlace señala el cambio de control de 1975, no su fundación ni la unificación formal de 1976. CShapes no ofrece una geometría separada de esta administración en 1975.", "vietnam-union")
relation("vsr-vnm", "VSR", "República de Vietnam del Sur · Gobierno Revolucionario Provisional", 1975, "VNM", "Vietnam unificado", 1976,
         "1976-07-02", "unification", "Unificación de las dos administraciones vietnamitas",
         "La entidad sureña provisional se distingue de la República de Vietnam anterior y de Vietnam del Norte. La unificación formal no se fecha en la caída de Saigón de abril de 1975.", "vietnam-union")

payload = {
    "retrieved": REFERENCE, "referenceDate": REFERENCE,
    "format": "country-history-relations", "license": "Original Spanish summaries; linked institutional sources retain their own terms. No source media reproduced.",
    "coverage": "Curated transitions and constitutional frameworks; incomplete worldwide and not a complete legal succession register.",
    "intervals": "Record start inclusive, end exclusive; missing end capped at referenceDate. Relation date is the labelled historical event, not the map anchor year.",
    "sources": [{"id": key, "url": value[0], "label": value[1]} for key, value in SOURCES.items()],
    "relations": relations, "records": records,
}
assert len({r["id"] for r in relations}) == len(relations)
assert len({r["id"] for r in records}) == len(records)
for item in records:
    assert item.get("end", "9999-12-31") > item["start"]
destination = ROOT / "public/data/country-history.json"
destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"{len(relations)} relations; {len(records)} records; {len(SOURCES)} sources -> {destination}")
