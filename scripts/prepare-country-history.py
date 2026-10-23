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
