# -*- coding: utf-8 -*-
"""
Labellift platform - genereert alle hoofdstukpagina's (web + PDF-bron) + index.html
uit een centrale inhoudsbron. Output is gewone, bewerkbare HTML.

Draaien:  <python> build-pages.py     (volledige pad naar python.exe)
Daarna:   build-pdf.ps1               (om de PDF's te (her)genereren)
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))

GOLD_DEFAULT = ("Ga vóór aanschaf en montage na of het product in de aangeboden opstelling bekend is "
                "bij het BCRG-register. Dan mag de adviseur de gunstige, productspecifieke waarde "
                "overnemen. Zo niet, dan geldt een voorzichtige forfaitaire waarde.")

CHAPTERS = [
 {
  "slug":"dak","icon":"🏠","group":"Schil","title":"Dak",
  "lead":"Het dak is vaak je grootste warmteverliespost — en meestal goed te documenteren. Met sterk bewijs telt je dakisolatie mee voor de échte waarde.",
  "card":"Dakisolatie en daktype — vaak de grootste warmtewinst.",
  "waarom":"Het dak is vaak je grootste warmteverliespost, dus goede dakisolatie levert direct comfort én een beter label op. De adviseur rekent alleen met de werkelijke isolatie als je die kunt <b>aantonen</b> — en omdat de <b>isolatiewaarde wordt bepaald door de dikte</b>, draait alles om het vastleggen van materiaal én dikte. Kun je niets aantonen, dan gaat de adviseur uit van de isolatie die bij het bouwjaar hoort: woningen van vóór 1966 tellen dan als <b>ongeïsoleerd</b>, ook al is er later na-geïsoleerd.",
  "herkennen":"Dakisolatie zie je vaak vanaf de zolder of bij een onbeschoten kap: tussen of onder de spanten, of als platen/dekens tegen het dakbeschot. Let op of het om <b>binnen-</b> of <b>buitenisolatie</b> gaat, en probeer altijd de <b>dikte</b> in beeld te krijgen.",
  "types":[("Hellende daken:","zadeldak, schilddak, mansardedak, lessenaarsdak, tentdak, wolfsdak, samengesteld dak."),
           ("Platte daken:","warm dak, koud dak, omgekeerd dak."),
           ("Bijzondere vormen:","tongewelf, vlinderdak, shedkap.")],
  "factuur":[("Bouwdeel:","dak — en of het binnen- of buitenisolatie betreft."),
             ("Wat is geïsoleerd:","duidelijk gespecificeerd dat (en welk deel van) het dak is geïsoleerd."),
             ("Merk en type","isolatiemateriaal."),
             ("Dikte (mm):","bepalend voor de isolatiewaarde — dus altijd vermelden."),
             ("Rc-/Rd-waarde","indien op de productverklaring vermeld."),
             ("Oppervlakte","(m²)."),
             ("KOMO-certificaat","of fabrieksgarantie van de leverancier, indien beschikbaar."),
             ("Adres:","factuur/leverbon op het adres van de woning.")],
  "foto_steps":["Overzichts-/locatiefoto: maak duidelijk wélk dakdeel het is (een herkenbaar punt of het zicht naar buiten).",
                "Detailfoto van de isolatielaag met een <b>rolmaat of duimstok</b> in beeld, zodat de dikte afleesbaar is.",
                "Foto van het etiket op de platen/dekens (merk, type, dikte) — herkenbaar als hetzelfde materiaal als op de overzichtsfoto."],
  "foto_imgs":[("overzicht","1 · Overzicht / locatie dakvlak"),("meetlat","2 · Dikte met rolmaat"),("detail","3 · Etiket (merk/type/dikte)")],
  "bewijssoorten":[("Factuur (en offerte):","waaruit blijkt wát is geïsoleerd en met welke dikte."),
                   ("Bouwtekeningen met isolatiediktes:","met het adres, de maker en het doel erop vermeld."),
                   ("Verklaring van een gecertificeerd isolatiebedrijf of een bouwkundig rapport:","met foto's waarop de dikte herleidbaar is en duidelijk wáár het materiaal zit."),
                   ("Oude foto's:","waarop het isolatiemateriaal én de dikte herleidbaar zichtbaar zijn.")],
  "goedfout":[("Foto van 14 cm isolatieplaten tussen de spanten met een duimstok ertegenaan + factuur met merk, type en dikte.","Foto van een afgewerkt plafond op zolder — daar is niet aan te zien wat eronder zit."),
              ("Factuur die specificeert dat het dak is geïsoleerd, mét dikte (mm) en oppervlakte.","\"Dak geïsoleerd\" zonder dikte — zonder dikte kan de isolatiewaarde niet worden bepaald."),
              ("Etiket leesbaar én herkenbaar als hetzelfde materiaal op de overzichtsfoto.","Losse, wazige close-up zonder dat duidelijk is wáár het zit.")],
  "fouten":["Geen maat in beeld — zonder rolmaat/duimstok is de dikte (en dus de isolatiewaarde) niet vast te stellen.","Alleen een detailfoto zonder overzicht — dan is niet duidelijk wélk dak het is.","Factuur zonder dikte of zonder adres van de woning.","Etiket onleesbaar of niet te koppelen aan de overzichtsfoto."],
  "forfaitair":"Geen bewijs? Dan rekent de adviseur met de isolatie die bij het bouwjaar hoort. Vóór 1966 golden er geen isolatie-eisen (de woning telt dan als ongeïsoleerd); vanaf de jaren zeventig wordt een minimale mate van isolatie aangenomen. Is er later na-geïsoleerd maar is dat tijdens de opname niet zichtbaar? Dan is aanvullend bewijs nodig om het mee te tellen.",
  "checklist":["Overzichts-/locatiefoto van het dakvlak gemaakt","Detailfoto van de isolatielaag mét rolmaat/duimstok (dikte zichtbaar)","Etiket leesbaar gefotografeerd (merk, type, dikte)","Factuur/leverbon met merk, type, dikte en adres","KOMO-certificaat/fabrieksgarantie bewaard, indien beschikbaar","Bewijs per onderdeel in een aparte map verzameld","Vooraf gecontroleerd of het materiaal bij BCRG bekend is"],
 },
 {
  "slug":"gevels","icon":"🧱","group":"Schil","title":"Gevels",
  "lead":"Isolatie in je muren zie je van buiten zelden. Dit onderdeel leunt daarom sterk op administratief bewijs — een goede factuur is goud waard.",
  "card":"Spouw- en gevelisolatie, binnen en buiten.",
  "waarom":"Gevelisolatie kan een groot verschil maken voor je label, maar is achteraf lastig zichtbaar. Zonder factuur of zichtbaar bewijs rekent de adviseur met de isolatiewaarde die bij het bouwjaar hoort — een woning van vóór 1976 wordt dan als ongeïsoleerd gerekend, ook als de spouw later wél is gevuld.",
  "herkennen":"De meeste woningen hebben een spouwmuur die later is na-geïsoleerd (ingeblazen). Soms is er binnen- of buitenisolatie aangebracht. Een doorsnede is soms zichtbaar bij een doorvoer, meterkast of open stopcontact in de buitenmuur, of tijdens een verbouwing.",
  "types":[("Spouwisolatie:","ingeblazen materiaal (EPS-parels, minerale wol, PUR) in de spouw."),
           ("Binnenisolatie:","na-isolatie aan de binnenzijde van de gevel."),
           ("Buitenisolatie:","isolatie aan de buitenzijde, met een nieuwe afwerklaag.")],
  "factuur":[("Bouwdeel:","gevel — spouw, binnen- of buitenisolatie."),
             ("Materiaal:","merk en type (bv. EPS-parels, minerale wol, PUR)."),
             ("Dikte / spouwbreedte","(mm) en <b>Rd-waarde</b> indien vermeld."),
             ("Oppervlakte","(m²) en <b>montagewijze</b> (bv. ingeblazen)."),
             ("Certificaat:","na-isolatiecertificaat of opleverrapport (vaak met endoscoop-foto's) is het sterkste bewijs."),
             ("Adres:","factuur op het adres van de woning.")],
  "foto_steps":["Overzichtsfoto van de gevel(s) van je woning.",
                "Detailfoto van een zichtbare doorsnede mét meetlat (spouwbreedte + materiaal), indien aanwezig.",
                "Foto van de vulgaten in de gevel (de boorgaten waardoor is ingespoten) bij na-isolatie."],
  "foto_imgs":[("overzicht","1 · Overzicht gevel(s)"),("meetlat","2 · Doorsnede met meetlat"),("detail","3 · Vulgaten / certificaat")],
  "bewijssoorten":[("Factuur (en offerte):","met materiaal, dikte/spouwbreedte en wat er is geïsoleerd."),
                   ("Na-isolatiecertificaat of opleverrapport:","vaak met endoscoop-foto's van de gevulde spouw — het sterkste bewijs."),
                   ("Bouwtekeningen met isolatiediktes:","met het adres, de maker en het doel erop vermeld."),
                   ("Oude foto's of een bouwkundig rapport:","waarop materiaal en dikte herleidbaar zijn en duidelijk is wáár het zit.")],
  "fouten":["Alleen een gevelfoto van buiten — daaraan is de isolatie niet af te lezen.","Factuur zonder dikte/spouwbreedte of zonder materiaal.","Geen adres op de bon (niet herleidbaar naar de woning).","Vulgaten of na-isolatiecertificaat niet bewaard."],
  "goedfout":[("Factuur \"spouwmuurisolatie 60 m², minerale wol, ingeblazen\" + opleverrapport met endoscoop-foto's.","Een mondelinge mededeling \"de vorige eigenaar heeft het laten doen\", zonder papier of foto."),
              ("Detailfoto van de spouw met meetlat waarop materiaal en breedte zichtbaar zijn.","Alleen een gevelfoto van buiten zonder enige onderbouwing."),
              ("Na-isolatiecertificaat op naam/adres van de woning.","Anonieme bon zonder adres of materiaalvermelding.")],
  "forfaitair":"Zonder factuur of zichtbaar bewijs geldt de isolatiewaarde van het bouwjaar. Bij oudere woningen pakt dat ongunstig uit. Heb je een na-isolatiecertificaat? Dat is hét bewijs — bewaar het zorgvuldig.",
  "checklist":["Overzichtsfoto van de gevel(s)","Detailfoto doorsnede met meetlat (indien zichtbaar)","Foto's van de vulgaten bij na-isolatie","Factuur/opdrachtbevestiging met materiaal en dikte/spouwbreedte","Na-isolatiecertificaat of opleverrapport bewaard","Factuur op het adres van de woning"],
 },
 {
  "slug":"vloer","icon":"🔲","group":"Schil","title":"Vloer",
  "lead":"De begane-grondvloer is meestal te bereiken via de kruipruimte. Een kruipluik en een zaklamp doen wonderen voor je bewijs.",
  "card":"Vloer- en bodemisolatie via de kruipruimte.",
  "waarom":"Een geïsoleerde vloer telt mee voor je label — als je het kunt aantonen. Geen toegang tot de kruipruimte en geen factuur? Dan rekent de adviseur met de bouwjaarwaarde, meestal \"ongeïsoleerd\".",
  "herkennen":"Vanuit de kruipruimte zie je de onderkant van de vloer. Isolatie kan bestaan uit platen of dekens tegen de vloer, ingespoten schuim, of een bodemafdekking op de kruipruimtebodem. Let op het verschil tussen <b>vloerisolatie</b> en <b>bodemisolatie</b>.",
  "types":[("Vloerisolatie:","platen of dekens tegen de onderkant van de vloer, of ingespoten."),
           ("Bodemisolatie:","afdekking op de bodem van de kruipruimte."),
           ("Geen kruipruimte:","bij een vloer op zand/beton is isolatie soms alleen via de factuur aantoonbaar.")],
  "factuur":[("Bouwdeel:","vloer of bodem — benoem dit expliciet (dat scheelt verwarring)."),
             ("Materiaal:","merk en type isolatiemateriaal."),
             ("Dikte","(mm) en <b>Rd-waarde</b> indien vermeld."),
             ("Oppervlakte","(m²) en <b>montagewijze</b>."),
             ("Adres:","factuur op het adres van de woning.")],
  "foto_steps":["Foto vanuit de kruipruimte van de onderkant van de vloer, waarop de isolatie zichtbaar is.",
                "Detailfoto van de isolatielaag mét meetlat voor de dikte.",
                "Foto waarop het type isolatie herkenbaar is (platen, dekens, schuim of bodemafdekking)."],
  "foto_imgs":[("overzicht","1 · Onderkant vloer (kruipruimte)"),("meetlat","2 · Dikte met meetlat"),("detail","3 · Type isolatie")],
  "bewijssoorten":[("Factuur (en offerte):","met materiaal, dikte en de vermelding vloer- of bodemisolatie."),
                   ("Foto's uit de kruipruimte:","met rolmaat, waarop de dikte herleidbaar is en duidelijk de onderkant van de vloer."),
                   ("Bouwtekeningen met isolatiediktes:","met het adres, de maker en het doel erop vermeld."),
                   ("Verklaring isolatiebedrijf of bouwkundig rapport:","met herleidbare dikte en duidelijke locatie.")],
  "fouten":["Foto van de vloerbedekking van bovenaf — daaraan is niets af te lezen.","Geen maat in beeld (de dikte is dan niet vast te stellen).","Factuur zonder dikte of zonder vermelding vloer/bodem.","Onduidelijk of het om de begane-grondvloer gaat."],
  "goedfout":[("Foto uit de kruipruimte van isolatieplaten tegen de vloer, met meetlat, plus factuur.","Foto van je vloerbedekking van bovenaf — daar valt niets aan af te lezen."),
              ("Factuur met materiaal, dikte en vermelding vloer/bodem.","\"Vloer geïsoleerd\" zonder materiaal of dikte."),
              ("Duidelijk in beeld dat het om de begane-grondvloer gaat.","Losse close-up zonder context.")],
  "forfaitair":"Geen toegang tot de kruipruimte en geen factuur? Dan geldt de bouwjaarwaarde, meestal \"ongeïsoleerd\". Een factuur met materiaal en dikte is dan je sterkste kaart.",
  "checklist":["Foto onderkant vloer vanuit de kruipruimte","Detailfoto met meetlat (dikte zichtbaar)","Type isolatie herkenbaar gefotografeerd","Factuur met materiaal, dikte en vloer/bodem-vermelding","Factuur op het adres van de woning"],
 },
 {
  "slug":"ramen-deuren-panelen","icon":"🪟","group":"Schil","title":"Ramen, deuren & panelen",
  "lead":"Het type glas heeft grote invloed op je label. Hier kun je vaak zelf al veel vaststellen — tot aan de code op de afstandhouder.",
  "card":"Glastype, kozijnen en panelen in het kozijn.",
  "waarom":"Glas, deuren en panelen in het kozijn bepalen samen een flink deel van het warmteverlies. Zonder bewijs schat de adviseur het glastype op basis van het bouwjaar — heb je later HR++-glas laten plaatsen maar kun je dat niet aantonen, dan kan het als ouder dubbelglas worden gerekend.",
  "herkennen":"Glas: enkel, dubbel, HR, HR+, HR++ of triple. Op de <b>afstandhouder</b> (het randje tussen de glasplaten) staat soms een code of jaartal. Met een vlammetje/pen tel je de reflecties om enkel/dubbel/triple te onderscheiden. Een <b>paneel</b> is een dicht deel in het kozijn (isolatiemateriaal + dikte zijn bepalend). Moderne <b>deuren</b> hebben een codering met de isolatiewaarde.",
  "types":[("Glas:","enkel / dubbel / HR / HR+ / HR++ / triple."),
           ("Panelen:","borstwerings- of deurpanelen — dicht deel in het kozijn."),
           ("Deuren:","met typeplaatje/codering waaruit de U-waarde blijkt.")],
  "factuur":[("Glas:","glassoort (HR++, triple), U-waarde (Ug), g-waarde, afmetingen of aantal ruiten, merk, datum."),
             ("Panelen:","merk/type, isolatiemateriaal, dikte (mm), U-waarde indien bekend."),
             ("Deuren:","merk/type, U-waarde (via codering), isolatiemateriaal en dikte indien bekend."),
             ("Adres:","factuur op het adres van de woning.")],
  "foto_steps":["Overzichtsfoto per gevel zodat duidelijk is welke ramen/deuren waar zitten.",
                "Detailfoto van de afstandhouder met code/jaartal (glas) of van de coderingssticker (deur).",
                "Detailfoto van een paneel in het kozijn met het etiket/de specificatie."],
  "foto_imgs":[("overzicht","1 · Overzicht per gevel"),("detail","2 · Afstandhouder / codering"),("detail","3 · Paneel / etiket")],
  "bewijssoorten":[("Factuur/leverbon:","met glastype (HR++/triple), U-waarde, merk en aantal/afmetingen, op adres."),
                   ("Productspecificatie:","van glas, kozijn of deur met de U-waarde."),
                   ("Foto van de afstandhouder:","met de code/het jaartal tussen de glasplaten."),
                   ("Detailfoto codering deur / etiket paneel:","waaruit type en isolatiewaarde blijken.")],
  "fouten":["\"Alle ramen vervangen\" zonder glastype op de bon.","Geen overzicht per gevel (onduidelijk welk raam waar zit).","Afstandhouder-code of deurcodering niet leesbaar.","Paneel zonder isolatiemateriaal/dikte."],
  "goedfout":[("Factuur \"HR++ beglazing, 8 ruiten\" + foto van de afstandhouder met productcode.","\"Alle ramen zijn vervangen\" zonder vermelding van het glastype."),
              ("Detailfoto waarop de codering van de deur leesbaar is.","Foto van een deur van te ver, zonder zichtbare codering."),
              ("Paneel-etiket met isolatiemateriaal en dikte in beeld.","\"Nieuwe kozijnen\" zonder specificaties.")],
  "forfaitair":"Zonder bewijs schat de adviseur het glas- en kozijntype op basis van het bouwjaar. Een factuur met glastype én een foto van de afstandhouder vormen samen sterk bewijs.",
  "checklist":["Overzichtsfoto per gevel","Detailfoto afstandhouder (glascode) of deurcodering","Detailfoto paneel met etiket/specificatie","Factuur met glastype, U-waarde en aantal/afmetingen","Specificaties van deuren en panelen vastgelegd","Factuur op het adres van de woning"],
 },
 {
  "slug":"ventilatie","icon":"💨","group":"Installatie","title":"Ventilatie",
  "lead":"Het ventilatiesysteem bepaalt mede hoe efficiënt je woning met warmte omgaat. Het gaat erom welk type je hebt.",
  "card":"Natuurlijk, mechanisch of WTW met warmteterugwinning.",
  "waarom":"Een systeem met warmteterugwinning (WTW) telt gunstiger mee dan natuurlijke of eenvoudige mechanische ventilatie. Zonder bewijs gaat de adviseur uit van het meest voorkomende systeem voor het bouwjaar — meestal ongunstiger dan wat je werkelijk hebt.",
  "herkennen":"Kijk naar de unit (vaak op zolder of in een kast) en naar de ventielen/roosters in huis: natuurlijke ventilatie (roosters, klepraampjes), mechanische afzuiging (afzuigbox met afvoer), of balansventilatie met WTW (aan- én afvoerkanalen).",
  "types":[("Natuurlijk:","roosters en klepraampjes, geen mechanische unit."),
           ("Mechanische afzuiging (C):","afzuigbox met afvoer."),
           ("Gebalanceerd (D) / WTW:","aan- en afvoer met warmteterugwinning.")],
  "factuur":[("Unit:","merk en type van de ventilatie-unit."),
             ("Systeemtype:","natuurlijk, mechanisch (C), gebalanceerd (D) of WTW."),
             ("WTW-rendement","(%) indien op de productspecificatie vermeld."),
             ("Adres:","factuur/installatierapport op het adres van de woning.")],
  "foto_steps":["Foto van de ventilatie-unit inclusief het typeplaatje (recht van voren, leesbaar).",
                "Foto's van de ventielen/roosters in de woning, zodat het systeemtype herkenbaar is.",
                "Bij WTW: foto waarop de aan- én afvoerkanalen zichtbaar zijn."],
  "foto_imgs":[("detail","1 · Typeplaatje unit"),("overzicht","2 · Ventielen / roosters"),("detail","3 · WTW-kanalen")],
  "bewijssoorten":[("Factuur of installatierapport:","met merk en type van de unit, op het adres van de woning."),
                   ("Foto van het typeplaatje:","van de ventilatie-unit (recht van voren, leesbaar)."),
                   ("Productspecificatie:","met het WTW-rendement bij balansventilatie."),
                   ("Inregelverklaring ventilatie:","indien beschikbaar.")],
  "fouten":["Foto van een rooster zonder dat het systeemtype blijkt.","Geen typeplaatje (merk/type onbekend).","WTW-rendement niet vastgelegd.","Een afzuigkap in de keuken verward met het ventilatiesysteem."],
  "goedfout":[("Foto van het typeplaatje van een WTW-unit + de installatiefactuur.","Een foto van een rooster zonder dat duidelijk is of er een mechanisch systeem achter zit."),
              ("Installatierapport met merk, type en rendement.","\"Mechanische ventilatie aanwezig\" zonder merk/type."),
              ("Duidelijk zichtbaar systeemtype (C, D of WTW).","Losse foto van een afzuigkap in de keuken.")],
  "forfaitair":"Zonder bewijs gaat de adviseur uit van het standaardsysteem voor het bouwjaar — meestal natuurlijke of eenvoudige mechanische ventilatie. Heb je WTW? Leg dat vast met typeplaatje en factuur.",
  "checklist":["Foto typeplaatje ventilatie-unit","Foto's ventielen/roosters (systeemtype herkenbaar)","Bij WTW: aan- en afvoerkanalen in beeld","Factuur/installatierapport met merk en type","WTW-rendement vastgelegd indien van toepassing","Factuur op het adres van de woning"],
 },
 {
  "slug":"verwarming","icon":"🔥","group":"Installatie","title":"Verwarming",
  "lead":"Je verwarmingstoestel is bijna altijd goed te documenteren — het typeplaatje vertelt het meeste.",
  "card":"Cv-ketel, warmtepomp, stadsverwarming.",
  "waarom":"Het rendement van je verwarming weegt zwaar mee. Geen typeplaatje en geen factuur? Dan schat de adviseur het keteltype en -rendement op basis van het bouwjaar van de woning, niet van de ketel. Een nieuwe HR-ketel in een oude woning wordt dan onterecht laag gerekend.",
  "herkennen":"Kijk naar het toestel: cv-ketel (HR107), warmtepomp (lucht/water of bodem), stadsverwarming (afleverset) of elektrische verwarming. Let ook op de afgifte: radiatoren, convectoren of vloerverwarming — vloerverwarming op lage temperatuur telt gunstiger.",
  "types":[("Cv-ketel:","merk, type, bouwjaar (bv. HR107)."),
           ("Warmtepomp:","lucht/water of bodem; prestatie via COP/SCOP."),
           ("Overig:","stadsverwarming (afleverset) of elektrische verwarming.")],
  "factuur":[("Cv-ketel:","merk, type/typenummer, vermogen (kW), bouwjaar, toestelsoort."),
             ("Warmtepomp:","merk, type, vermogen (kW), bron (lucht/water), COP/SCOP."),
             ("Afgifte:","radiatoren of vloerverwarming (lage temperatuur)."),
             ("Adres:","aankoop-/installatiefactuur op het adres van de woning.")],
  "foto_steps":["Foto van het typeplaatje van de cv-ketel (recht van voren, alle tekst leesbaar: merk, type, bouwjaar).",
                "Overzichtsfoto van de ketel/het toestel zodat het type herkenbaar is.",
                "Bij warmtepomp: typeplaatje van de binnen- én buitenunit; en foto's van de afgifte (radiator/vloerverwarming)."],
  "foto_imgs":[("detail","1 · Typeplaatje ketel"),("overzicht","2 · Overzicht toestel"),("detail","3 · Warmtepomp / afgifte")],
  "bewijssoorten":[("Typeplaatje-foto:","van de cv-ketel of warmtepomp (merk, type, bouwjaar — recht van voren)."),
                   ("Aankoop-/installatiefactuur:","bevestigt het bouwjaar en het type, op het adres van de woning."),
                   ("Datasheet/productspecificatie:","met het rendement (HR-klasse, COP/SCOP)."),
                   ("Inregelverklaring ruimteverwarming:","indien beschikbaar.")],
  "fouten":["Foto van de mantel zonder leesbaar typeplaatje.","Geen bouwjaar/installatiedatum (rendement valt dan op het woningbouwjaar terug).","Warmtepomp zonder COP/SCOP.","Geen onderscheid tussen radiatoren en vloerverwarming."],
  "goedfout":[("Scherpe foto van het typeplaatje (merk + type + jaar) + installatiefactuur.","Foto van de witte mantel van de ketel zonder dat het typeplaatje leesbaar is."),
              ("Warmtepomp: beide units met typeplaatjes + datasheet met SCOP.","\"Warmtepomp aanwezig\" zonder type of prestatiecijfer."),
              ("Vloerverwarming aangetoond met factuur/tekening (lage temperatuur).","Geen onderscheid tussen radiatoren en vloerverwarming.")],
  "forfaitair":"Zonder typeplaatje en factuur rekent de adviseur op basis van het bouwjaar van de woning. Juist een recente, zuinige installatie verdient sterk bewijs om mee te tellen.",
  "checklist":["Scherpe foto typeplaatje ketel (merk/type/jaar)","Overzichtsfoto van het toestel","Warmtepomp: typeplaatjes binnen- én buitenunit","Datasheet met COP/SCOP (warmtepomp)","Installatiefactuur op het adres van de woning","Afgiftesysteem (radiator/vloerverwarming) vastgelegd"],
  "extra_callout":("Hybride opstelling?","Een hybride (cv-ketel + warmtepomp) telt vaak als combinatie/opstelling. Controleer bij BCRG de combinatie zoals aangeboden, niet alleen de losse onderdelen."),
 },
 {
  "slug":"tapwater","icon":"🚿","group":"Installatie","title":"Tapwater",
  "lead":"Hoe je warm water maakt, telt mee voor je label. Het draait om het type toestel en het rendement.",
  "card":"Combiketel, boiler, warmtepompboiler, zonneboiler.",
  "waarom":"Warmwaterbereiding is onderdeel van de energieberekening. Zonder bewijs gaat de adviseur uit van het meest voorkomende toestel voor het bouwjaar — een zuinig toestel telt dan niet mee zoals het hoort.",
  "herkennen":"Bepaal of het warme water komt uit de cv-combiketel, een (elektrische) boiler, een warmtepompboiler of een zonneboiler (collector op het dak + voorraadvat). Vaak staat op de cv-ketel of het toestel of het ook voor tapwater wordt gebruikt.",
  "types":[("Cv-combi:","de cv-ketel maakt ook warm water."),
           ("Boiler:","elektrische boiler met voorraadvat."),
           ("Warmtepompboiler:","zuinige boiler met warmtepomp; prestatie via COP."),
           ("Zonneboiler:","collector op het dak + voorraadvat.")],
  "factuur":[("Toestel:","merk en type."),
             ("Capaciteit:","inhoud voorraadvat (liter)."),
             ("Prestatie:","COP bij warmtepompboiler; collectoroppervlak + vat bij zonneboiler."),
             ("Adres:","factuur/installatierapport op het adres van de woning.")],
  "foto_steps":["Foto van het typeplaatje van het tapwatertoestel (recht van voren, leesbaar).",
                "Overzichtsfoto van het toestel/de opstelling.",
                "Bij zonneboiler: foto van de collector op het dak én het voorraadvat."],
  "foto_imgs":[("detail","1 · Typeplaatje toestel"),("overzicht","2 · Overzicht opstelling"),("detail","3 · Collector / voorraadvat")],
  "bewijssoorten":[("Typeplaatje-foto:","van het tapwatertoestel (combi, boiler, warmtepompboiler of zonneboiler)."),
                   ("Factuur of installatierapport:","met merk, type en capaciteit (liter), op het adres van de woning."),
                   ("Productspecificatie:","met COP (warmtepompboiler) of collectoroppervlak (zonneboiler)."),
                   ("Inregelverklaring tapwater:","indien beschikbaar.")],
  "fouten":["\"Boiler aanwezig\" zonder merk, type of inhoud.","Onduidelijk of de cv-ketel ook tapwater levert (combi).","Zonneboiler zonder collectoroppervlak of vat.","Geen typeplaatje van het toestel."],
  "goedfout":[("Foto van het typeplaatje van een warmtepompboiler + de factuur met capaciteit.","\"Boiler aanwezig\" zonder merk, type of inhoud."),
              ("Zonneboiler: collector op dak + voorraadvat + factuur.","Alleen \"zonneboiler\" zonder collectoroppervlak of vat."),
              ("Aangetoond dat de cv-ketel ook tapwater levert (combi).","Onduidelijk of het toestel verwarming én tapwater doet.")],
  "forfaitair":"Zonder typegegevens valt de adviseur terug op een standaardaanname voor het bouwjaar. Leg merk, type en capaciteit vast met een foto van het typeplaatje en de factuur.",
  "checklist":["Foto typeplaatje tapwatertoestel","Overzichtsfoto van de opstelling","Zonneboiler: collector én voorraadvat in beeld","Factuur met merk, type en capaciteit (liter)","COP/collectoroppervlak vastgelegd indien van toepassing","Factuur op het adres van de woning"],
 },
 {
  "slug":"koeling","icon":"❄️","group":"Installatie","title":"Koeling",
  "lead":"Actieve koeling telt mee in de energieberekening. Het type en het rendement bepalen hoe het meeweegt.",
  "card":"Airco of warmtepomp met koelfunctie.",
  "waarom":"Heb je actieve koeling, dan hoort die in de berekening thuis. Zonder bewijs kan de adviseur het type en rendement niet goed meenemen, wat ongunstig of onnauwkeurig uitpakt.",
  "herkennen":"Koeling kan een split-unit airco zijn (binnen- + buitenunit) of een warmtepomp met koelfunctie. Soms is er geen actieve koeling. Het typeplaatje op de buitenunit geeft merk, type en vermogen.",
  "types":[("Geen:","geen actieve koeling aanwezig."),
           ("Airco (split-unit):","binnen- en buitenunit."),
           ("Warmtepomp met koelfunctie:","dezelfde unit verwarmt én koelt.")],
  "factuur":[("Toestel:","merk en type."),
             ("Vermogen:","koelvermogen (kW)."),
             ("Rendement:","SEER/koelrendement indien bekend."),
             ("Adres:","factuur op het adres van de woning.")],
  "foto_steps":["Foto van het typeplaatje van de buitenunit (recht van voren, leesbaar).",
                "Foto van de binnenunit(s).",
                "Overzichtsfoto zodat duidelijk is of het airco of een warmtepomp met koelfunctie is."],
  "foto_imgs":[("detail","1 · Typeplaatje buitenunit"),("overzicht","2 · Binnenunit"),("detail","3 · Overzicht opstelling")],
  "bewijssoorten":[("Typeplaatje-foto:","van de buiten- en binnenunit (merk, type, vermogen)."),
                   ("Factuur of installatierapport:","op het adres van de woning."),
                   ("Productspecificatie:","met koelvermogen en rendement (SEER), indien bekend.")],
  "fouten":["Foto van de buitenunit van te ver, zonder typegegevens.","Onduidelijk of het airco of een warmtepomp met koelfunctie is.","Geen vermogen of rendement vastgelegd."],
  "goedfout":[("Foto's van beide units met typeplaatjes + de factuur.","Foto van de buitenunit van een afstand, zonder typegegevens."),
              ("Duidelijk of het airco of warmtepomp met koelfunctie betreft.","\"Airco aanwezig\" zonder merk of vermogen."),
              ("Vermogen/rendement vastgelegd via typeplaatje of datasheet.","Geen enkele specificatie van de koeling.")],
  "forfaitair":"Zonder bewijs kan koeling niet goed worden meegenomen. Leg merk, type en vermogen vast met een foto van het typeplaatje en de factuur.",
  "checklist":["Foto typeplaatje buitenunit","Foto binnenunit(s)","Overzichtsfoto opstelling","Factuur met merk, type en vermogen","Rendement (SEER) vastgelegd indien bekend","Factuur op het adres van de woning"],
 },
 {
  "slug":"zonne-energie","icon":"☀️","group":"Installatie","title":"Zonne-energie (PV)",
  "lead":"Zonnepanelen tellen mee voor je label op basis van het opgewekte vermogen. Daarvoor zijn aantal en wattage doorslaggevend.",
  "card":"Zonnepanelen (PV): aantal, merk en vermogen.",
  "waarom":"PV-panelen verlagen je energiebehoefte op papier — mits je het vermogen kunt aantonen. Kun je het vermogen niet aantonen, dan schat de adviseur het aantal van een foto, maar blijft het exacte wattage onzeker en wordt het voorzichtig ingeschat.",
  "herkennen":"Tel de panelen op het dak en zoek de omvormer (vaak in de meterkast of op zolder). Op de achterkant van een paneel en op de omvormer staat een typeplaatje met de specificaties.",
  "types":[("Panelen:","aantal × wattpiek (Wp) per paneel."),
           ("Omvormer:","merk en type."),
           ("Oriëntatie:","ligging en hellingshoek indien bekend.")],
  "factuur":[("Panelen:","merk en type, aantal, vermogen per paneel (Wp), totaal (kWp)."),
             ("Omvormer:","merk en type."),
             ("Ligging:","oriëntatie en hellingshoek indien bekend."),
             ("Adres:","aankoop-/installatiefactuur op het adres van de woning.")],
  "foto_steps":["Overzichtsfoto van het dak met de panelen, waarop je het aantal kunt tellen.",
                "Foto van de omvormer met typeplaatje (recht van voren, leesbaar).",
                "Indien mogelijk: foto van het typeplaatje op de achterkant van een paneel (met het wattage)."],
  "foto_imgs":[("overzicht","1 · Dak met panelen (telbaar)"),("detail","2 · Typeplaatje omvormer"),("detail","3 · Typeplaatje paneel")],
  "bewijssoorten":[("Aankoop-/installatiefactuur:","met aantal panelen, Wp per paneel en totaal kWp, op het adres van de woning."),
                   ("Typeplaatje-foto paneel:","op de achterkant (merk, type, wattage)."),
                   ("Foto van de omvormer:","met het typeplaatje leesbaar."),
                   ("Dakfoto:","waarop het aantal panelen telbaar is.")],
  "fouten":["\"We hebben zonnepanelen\" zonder aantal of vermogen.","Dakfoto van te ver (panelen niet te tellen).","Typeplaatje van omvormer of paneel niet leesbaar.","Geen factuur met Wp/kWp."],
  "goedfout":[("Factuur \"10 panelen × 400 Wp\" + dakfoto waarop je 10 panelen telt + foto omvormer.","\"We hebben zonnepanelen\" zonder aantal, vermogen of foto."),
              ("Typeplaatje omvormer en/of paneel leesbaar in beeld.","Dakfoto van te ver waarop de panelen niet te tellen zijn."),
              ("Totaal vermogen (kWp) herleidbaar uit de factuur.","Geen factuur en geen wattage bekend.")],
  "forfaitair":"Zonder factuur blijft het wattage onzeker en wordt het voorzichtig ingeschat. Met de factuur erbij telt elke watt mee.",
  "checklist":["Overzichtsfoto dak met telbare panelen","Foto typeplaatje omvormer","Foto typeplaatje paneel (indien bereikbaar)","Factuur met aantal × Wp en totaal kWp","Merk/type panelen en omvormer vastgelegd","Factuur op het adres van de woning"],
 },
 {
  "slug":"energieopslag","icon":"🔋","group":"Installatie","title":"Energieopslag",
  "lead":"Een thuisbatterij vergroot het eigen verbruik van je opgewekte stroom. Leg merk en capaciteit goed vast.",
  "card":"Thuisbatterij: merk en capaciteit.",
  "waarom":"Energieopslag is relatief nieuw en nog niet bij elke woning aanwezig. Wil je dat het meetelt, leg dan merk, capaciteit en vermogen vast — zonder gegevens kan het niet of slechts ongunstig worden meegenomen.",
  "herkennen":"De thuisbatterij is een aparte unit, vaak dicht bij de omvormer of in de meterkast/berging. Op de unit staat een typeplaatje met merk, capaciteit (kWh) en vermogen (kW).",
  "types":[("Thuisbatterij:","merk en type."),
           ("Capaciteit:","opslag in kWh."),
           ("Koppeling:","gekoppelde omvormer / PV-installatie.")],
  "factuur":[("Batterij:","merk en type."),
             ("Capaciteit:","opslagcapaciteit (kWh) en vermogen (kW)."),
             ("Koppeling:","gekoppelde omvormer indien van toepassing."),
             ("Adres:","factuur op het adres van de woning.")],
  "foto_steps":["Foto van het typeplaatje van de batterij-unit (merk, capaciteit, vermogen).",
                "Overzichtsfoto van de opstelling (batterij + eventuele omvormer).",
                "Foto waarop de koppeling met de PV-installatie zichtbaar is, indien van toepassing."],
  "foto_imgs":[("detail","1 · Typeplaatje batterij"),("overzicht","2 · Overzicht opstelling"),("detail","3 · Koppeling omvormer")],
  "bewijssoorten":[("Typeplaatje-foto:","van de batterij-unit (merk, capaciteit in kWh, vermogen in kW)."),
                   ("Aankoop-/installatiefactuur:","met merk, type en capaciteit, op het adres van de woning."),
                   ("Productspecificatie:","met capaciteit (kWh) en vermogen (kW).")],
  "fouten":["Foto van een kast zonder zichtbare gegevens.","\"Thuisbatterij aanwezig\" zonder specificatie.","Capaciteit (kWh) niet vastgelegd."],
  "goedfout":[("Foto van het typeplaatje + factuur met capaciteit in kWh.","Foto van een kast zonder zichtbare gegevens."),
              ("Merk, capaciteit en vermogen herleidbaar uit de factuur.","\"Thuisbatterij aanwezig\" zonder enige specificatie."),
              ("Koppeling met de PV-installatie aangetoond.","Onduidelijk of de batterij is aangesloten.")],
  "forfaitair":"Zonder gegevens kan de batterij niet of slechts ongunstig worden meegerekend. Een foto van het typeplaatje en de factuur met kWh maken het verschil.",
  "checklist":["Foto typeplaatje batterij-unit","Overzichtsfoto van de opstelling","Capaciteit (kWh) en vermogen (kW) vastgelegd","Factuur met merk en type","Koppeling met PV-installatie aangetoond","Factuur op het adres van de woning"],
 },
]

# ---------- bouwstenen ----------
def facts_html(items):
    out=['<ul class="facts">']
    for b,rest in items:
        out.append('  <li><b>%s</b> %s</li>'%(b,rest))
    out.append('</ul>')
    return "\n".join(out)

def types_html(items):
    if not items: return ""
    out=['<h3>Veelvoorkomende typen</h3>','<ul class="facts">']
    for b,rest in items:
        out.append('  <li><b>%s</b> %s</li>'%(b,rest))
    out.append('</ul>')
    return "\n".join(out)

def steps_html(steps):
    out=['<ol class="steps-photo">']
    for s in steps:
        out.append('  <li>%s</li>'%s)
    out.append('</ol>')
    return "\n".join(out)

import os
FOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "foto")

def photo_src(slug, idx, key, base):
    # Echte foto '<slug>-<slotnummer>.<ext>' gebruiken indien aanwezig, anders de placeholder.
    for ext in ("jpg","jpeg","png","webp","JPG","JPEG","PNG"):
        if os.path.exists(os.path.join(FOTO_DIR, "%s-%d.%s" % (slug, idx, ext))):
            return "%sassets/foto/%s-%d.%s" % (base, slug, idx, ext), True
    return "%sassets/foto/voorbeeld-%s.svg" % (base, key), False

def photos_html(imgs, base, slug):
    out=['<div class="photos">']
    for i,(key,cap) in enumerate(imgs, 1):
        src, real = photo_src(slug, i, key, base)
        alt = cap if real else "Voorbeeldfoto"
        out.append('  <figure class="photo"><img src="%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>'%(src, alt, cap))
    out.append('</div>')
    return "\n".join(out)

def photos_html_pdf(imgs, slug):
    out=['<div class="photos avoid-break">']
    for i,(key,cap) in enumerate(imgs, 1):
        src, real = photo_src(slug, i, key, "../")
        out.append('  <figure><img src="%s" alt=""><figcaption>%s</figcaption></figure>'%(src, cap))
    out.append('</div>')
    return "\n".join(out)

def gb_html(rows, web=True):
    head = '✅ Sterk bewijs' if web else 'Sterk bewijs'
    head2= '❌ Zwak of onbruikbaar' if web else 'Zwak of onbruikbaar'
    cls = 'gb' if web else 'gb avoid-break'
    out=['<table class="%s">'%cls,'  <thead><tr><th>%s</th><th>%s</th></tr></thead>'%(head,head2),'  <tbody>']
    for ok,no in rows:
        out.append('    <tr><td class="ok">%s</td><td class="no">%s</td></tr>'%(ok,no))
    out.append('  </tbody>'); out.append('</table>')
    return "\n".join(out)

def checklist_html(items, web=True):
    cls='checklist' if web else 'checklist avoid-break'
    out=['<ul class="%s">'%cls]
    for i in items: out.append('  <li>%s</li>'%i)
    out.append('</ul>')
    return "\n".join(out)

def extra_callout_web(ch):
    if "extra_callout" not in ch: return ""
    t,x = ch["extra_callout"]
    return ('<div class="callout"><div class="ic">💡</div><div><b>%s</b><p>%s</p></div></div>'%(t,x))

def extra_callout_pdf(ch):
    if "extra_callout" not in ch: return ""
    t,x = ch["extra_callout"]
    return ('<div class="callout avoid-break"><b>%s</b><p>%s</p></div>'%(t,x))

def bewijs_html(items):
    if not items: return ""
    return "<h2>Wat telt als bewijs?</h2>\n" + facts_html(items)

def fouten_html(items):
    if not items: return ""
    out=['<ul class="facts">']
    for i in items: out.append('  <li>%s</li>'%i)
    out.append('</ul>')
    return "<h2>Veelgemaakte fouten</h2>\n" + "\n".join(out)

def plain_list_html(items):
    out=['<ul class="facts">']
    for i in items: out.append('  <li>%s</li>'%i)
    out.append('</ul>')
    return "\n".join(out)

def acc(title, desc, body, is_open=False, wide=False):
    op = " open" if is_open else ""
    cls = "acc acc-wide" if wide else "acc"
    return ('<details class="%s"%s>\n'
            '  <summary><div class="acc-tt"><b>%s</b><span>%s</span></div>'
            '<span class="chev">▾</span></summary>\n'
            '  <div class="acc-body">\n%s\n  </div>\n'
            '</details>') % (cls, op, title, desc, body)

# ---------- web pagina ----------
def web_page(ch):
    gold = ch.get("gold", GOLD_DEFAULT)
    callout = ('<div class="callout"><div class="ic">🟢</div>'
               '<div><b>Gouden regel — controleer vóór aanschaf:</b><p>%s</p>'
               '<p style="margin:10px 0 0"><a class="btn btn-outline" '
               'href="https://bcrg.nl/nl/databanken/energieprestaties/databank/?ordering=-created_at&amp;search=&amp;page=1" '
               'target="_blank" rel="noopener">🔎 Zoek in de BCRG-databank</a></p>'
               '</div></div>') % gold
    secs = []
    secs.append(acc("Waarom dit telt", "Wat dit onderdeel oplevert voor je energielabel", "<p>%s</p>" % ch["waarom"]))
    secs.append(acc("Hoe herken je het", "Waar je het ziet en welke typen er zijn", "<p>%s</p>\n%s" % (ch["herkennen"], types_html(ch.get("types")))))
    secs.append(acc("Wat moet op de factuur", "Welke gegevens op de factuur of leverbon horen", facts_html(ch["factuur"])))
    fotobody = "%s\n%s\n%s" % (steps_html(ch["foto_steps"]), photos_html(ch["foto_imgs"], "../", ch["slug"]), extra_callout_web(ch))
    secs.append(acc("Welke foto's maak je", "De foto's die je voor je dossier maakt", fotobody, is_open=True, wide=True))
    if ch.get("bewijssoorten"):
        secs.append(acc("Wat telt als bewijs?", "Welke documenten en foto's meetellen", facts_html(ch["bewijssoorten"])))
    secs.append(acc("Sterk vs. zwak bewijs", "Voorbeelden van goed en onbruikbaar bewijs", gb_html(ch["goedfout"], True)))
    if ch.get("fouten"):
        secs.append(acc("Veelgemaakte fouten", "Valkuilen die je label onnodig kunnen drukken", plain_list_html(ch["fouten"])))
    secs.append(acc("Geen bewijs? Wat dan?", "Dan rekent de adviseur met het bouwjaar (forfaitair) — vaak ongunstiger", "<p>%s</p>" % ch["forfaitair"]))
    download = ('<div class="download-band"><div>'
                '<h3>📄 Download dit hoofdstuk als PDF</h3>'
                '<p>Handig om mee te nemen of door te sturen.</p></div>'
                '<a class="btn btn-download" href="../pdf/%s.pdf" download>PDF downloaden</a></div>') % ch["slug"]
    secs.append(acc("Checklist %s" % ch["title"].lower(), "Alles op een rij om af te vinken", checklist_html(ch["checklist"], True)))
    body = callout + '\n\n<div class="acc-grid">\n' + "\n".join(secs) + '\n</div>\n\n' + download
    return """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Labellift</title>
<meta name="description" content="{title} vastleggen voor je energielabel: hoe en waarom, wat op de factuur moet en welke foto's je maakt.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="../assets/logo.svg">
<link rel="stylesheet" href="../assets/labellift.css">
</head>
<body>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="../index.html"><img src="../assets/logo.svg" alt=""><span>Label</span><b>lift</b><span>.nl</span></a>
    <nav class="nav-links">
      <a href="../index.html#hoe">Hoe het werkt</a>
      <a href="../index.html#hoofdstukken">Onderwerpen</a>
      <a href="#" class="btn btn-teal">Start je dossier</a>
    </nav>
    <button class="menu-btn" aria-label="Menu">☰</button>
  </div>
  <div class="mobile-menu">
    <a href="../index.html#hoe">Hoe het werkt</a>
    <a href="../index.html#hoofdstukken">Onderwerpen</a>
    <a href="#">Start je dossier</a>
  </div>
</header>

<section class="chap-hero">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Onderwerpen</a> › {group} › {title}</div>
    <h1>{icon} {title}</h1>
    <p>{lead}</p>
  </div>
</section>

<div class="container" style="padding:30px 20px 10px">
  <article class="article">
{body}
  </article>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="brand"><img src="../assets/logo.svg" alt=""><span>Label</span><b>lift</b><span>.nl</span></div>
    <div class="small">Onafhankelijk verduurzamingsplatform · © <span data-year>2026</span> Labellift</div>
  </div>
</footer>
<script src="../assets/site.js"></script>
</body>
</html>
""".format(title=ch["title"], group=ch["group"], icon=ch["icon"], lead=ch["lead"], body=body)

# ---------- pdf bron ----------
def pdf_page(ch):
    gold = ch.get("gold", GOLD_DEFAULT)
    return """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title>Labellift — {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="print.css">
</head>
<body>

<div class="cover">
  <div class="brand"><img src="../assets/logo.svg" alt=""><span>Label<span class="teal">lift</span>.nl</span></div>
  <p class="kicker">Verduurzamingsgids · {group}</p>
  <h1>{title}</h1>
  <p>{lead}</p>
</div>

<h2>Waarom dit telt</h2>
<p>{waarom}</p>

<h2>Hoe herken je het</h2>
<p>{herkennen}</p>
{types}

<div class="callout avoid-break">
  <b>Gouden regel — controleer vóór aanschaf.</b>
  <p>{gold}</p>
</div>

<h2>Wat moet op de factuur</h2>
{factuur}

<h2>Welke foto's maak je</h2>
{steps}
{photos}
{extra}

{bewijs}

<h2>Sterk vs. zwak bewijs</h2>
{gb}

{fouten}

<h2>Wanneer forfaitair?</h2>
<p>{forfaitair}</p>

<h2>Checklist {title_l}</h2>
{checklist}

<div class="foot">Labellift.nl · Onafhankelijk verduurzamingsplatform · Dit document is een hulpmiddel; de EPA-adviseur beoordeelt per situatie welk bewijs volgens NTA 8800 en BRL 9500 bruikbaar is.</div>

</body>
</html>
""".format(
        title=ch["title"], title_l=ch["title"].lower(), group=ch["group"], lead=ch["lead"],
        waarom=ch["waarom"], herkennen=ch["herkennen"], types=types_html(ch.get("types")),
        gold=gold, factuur=facts_html(ch["factuur"]), steps=steps_html(ch["foto_steps"]),
        photos=photos_html_pdf(ch["foto_imgs"], ch["slug"]), extra=extra_callout_pdf(ch),
        bewijs=bewijs_html(ch.get("bewijssoorten")), fouten=fouten_html(ch.get("fouten")),
        gb=gb_html(ch["goedfout"], False), forfaitair=ch["forfaitair"],
        checklist=checklist_html(ch["checklist"], False))

# ---------- index ----------
def cards_for(group):
    out=[]
    for ch in CHAPTERS:
        if ch["group"]!=group: continue
        out.append("""      <a class="card" href="hoofdstukken/{slug}.html">
        <span class="badge live">Beschikbaar</span>
        <div class="icon">{icon}</div><h3>{title}</h3>
        <p>{card}</p>
        <span class="card-link">Lees verder →</span>
      </a>""".format(slug=ch["slug"], icon=ch["icon"], title=ch["title"], card=ch["card"]))
    return "\n".join(out)

def index_page():
    return """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Labellift — naar het beste energielabel, met bewijs</title>
<meta name="description" content="Labellift is een onafhankelijk platform dat pandeigenaren helpt het hoogst haalbare energielabel te halen door verduurzaming goed vast te leggen.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="assets/logo.svg">
<link rel="stylesheet" href="assets/labellift.css">
</head>
<body>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html"><img src="assets/logo.svg" alt=""><span>Label</span><b>lift</b><span>.nl</span></a>
    <nav class="nav-links">
      <a href="#hoe">Hoe het werkt</a>
      <a href="#hoofdstukken">Onderwerpen</a>
      <a href="#" class="btn btn-teal">Start je dossier</a>
    </nav>
    <button class="menu-btn" aria-label="Menu">☰</button>
  </div>
  <div class="mobile-menu">
    <a href="#hoe">Hoe het werkt</a>
    <a href="#hoofdstukken">Onderwerpen</a>
    <a href="#">Start je dossier</a>
  </div>
</header>

<section class="hero">
  <div class="container">
    <span class="badge-indep">● 100% onafhankelijk — geen productverkoop</span>
    <h1>Naar het beste energielabel — met bewijs dat telt</h1>
    <p>Labellift helpt pandeigenaren om slim en onafhankelijk te verduurzamen. Van eerste inzicht en nulmeting tot maatwerkadvies, uitvoering en definitief energielabel. Zo weet je vooraf welke maatregelen écht bijdragen aan het gewenste label en voorkom je onnodige kosten.</p>
    <div class="hero-actions">
      <a href="#hoofdstukken" class="btn btn-teal">Bekijk de onderwerpen</a>
      <a href="#hoe" class="btn btn-ghost">Hoe werkt het?</a>
    </div>
  </div>
</section>

<section class="block" id="hoe">
  <div class="container">
    <p class="eyebrow">Hoe het werkt</p>
    <h2 class="section-head">In drie stappen naar sterk bewijs</h2>
    <p class="section-sub">Voor elk onderdeel van je woning bouw je bewijs op. Hoe meer je aantoont, hoe nauwkeuriger en gunstiger je label.</p>
    <div class="steps">
      <div class="step"><span class="n">1</span><h3>Controleer vooraf</h3><p>Check vóór aanschaf of een product in de aangeboden opstelling bekend is bij het BCRG-register. Zo telt de gunstige productwaarde mee.</p></div>
      <div class="step"><span class="n">2</span><h3>Leg vast op de factuur</h3><p>Zorg dat merk, type, dikte, vermogen en oppervlakte op de factuur staan — herleidbaar naar jouw adres.</p></div>
      <div class="step"><span class="n">3</span><h3>Maak foto's voor je dossier</h3><p>Eén overzicht én één detail per onderdeel, met de maat (meetlat) of het typeplaatje leesbaar in beeld.</p></div>
    </div>
    <div class="callout">
      <div class="ic">🟢</div>
      <div><b>De gouden regel:</b><p>Mét aantoonbaar bewijs rekent de EPA-adviseur met de echte waarde. Zonder bewijs valt hij terug op een voorzichtige standaardwaarde op basis van het bouwjaar — bijna altijd ongunstiger. <em>Niet vastgelegd = niet meegerekend.</em></p></div>
    </div>
  </div>
</section>

<section class="block" id="hoofdstukken" style="padding-top:10px">
  <div class="container">
    <p class="eyebrow">De onderwerpen</p>
    <h2 class="section-head">Per onderdeel van je woning</h2>
    <p class="section-sub">Elk onderwerp legt uit: hoe &amp; waarom, hoe je het herkent, wat op de factuur moet en welke foto's je maakt. Met een downloadbare PDF per onderwerp.</p>

    <div class="group-title"><span class="dot"></span> Schil — de buitenkant van je woning</div>
    <div class="cards">
{schil}
    </div>

    <div class="group-title"><span class="dot"></span> Installatie — techniek in je woning</div>
    <div class="cards">
{installatie}
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="brand"><img src="assets/logo.svg" alt=""><span>Label</span><b>lift</b><span>.nl</span></div>
    <div class="small">Onafhankelijk verduurzamingsplatform · © <span data-year>2026</span> Labellift</div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
""".format(schil=cards_for("Schil"), installatie=cards_for("Installatie"))

# ---------- schrijven ----------
def write(path, content):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ->", os.path.relpath(path, HERE))

def main():
    os.makedirs(os.path.join(HERE,"hoofdstukken"), exist_ok=True)
    os.makedirs(os.path.join(HERE,"pdf-bron"), exist_ok=True)
    print("Hoofdstukpagina's:")
    for ch in CHAPTERS:
        write(os.path.join(HERE,"hoofdstukken",ch["slug"]+".html"), web_page(ch))
        write(os.path.join(HERE,"pdf-bron",ch["slug"]+".html"), pdf_page(ch))
    print("Index:")
    write(os.path.join(HERE,"index.html"), index_page())
    print("Klaar:", len(CHAPTERS), "hoofdstukken.")

if __name__=="__main__":
    main()
