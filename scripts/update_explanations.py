# -*- coding: utf-8 -*-
import json

with open('images.json', encoding='utf-8') as f:
    manifest = json.load(f)

explanations = {
    'img_3d6253e6eb.jpg': 'A fekete WC-ülőkelap logikátlanul elüt a fehér WC-től, és a tükröződések iránya sem egyezik a fényforrással.',
    'img_ebb6d2bc7e.jpg': 'A háttér tájkép festőien szép, drámai felhőzettel és tökéletesen elhelyezett fákkal — valódi fotón ez ritka.',
    'img_93969ecccb.jpg': 'A sárga buszon látható feliratok elmosódottak és olvashatatlanok, ami tipikus AI-artifakt szövegek közelében.',
    'img_c4b6035282.jpg': 'A parki padok és fák elrendezése túl szimmetrikus, a fa kérge rendellenes, elmosódott textúrával rendelkezik.',
    'img_70e3a3506f.jpg': 'A rendőrségi motorokon látható POLICE felirat minden motoron torz és más betűket mutat — az AI nem tudja helyesen renderelni a szövegeket.',
    'img_5412a25f05.jpg': 'Az idősebb pár lábai és cipői részben átfednek és deformált megjelenést mutatnak, a testarányok sem következetesek.',
    'img_696bd547d9.jpg': 'A közlekedési lámpán megjelenő piros fény körül valószerűtlen glória keletkezik, és az épületek ablakainak mintázata nem következetes.',
    'img_5968a20b15.jpg': 'A két fiú kalapja teljesen különböző színű (fehér és sárga), de szinte azonos alakzattal — ez a kép tükröző szimmetriájára utal.',
    'img_64129e251f.jpg': 'A nappali túl tökéletes és szimmetrikus, a bútorok elrendezése és a fény iránya fizikailag lehetetlen egy valódi térben.',
    'img_12f30ed8c1.jpg': 'A bicikli vázán nincs nyereg, csak az ülőrész ragasztéka, és a háttérben látható díszített oszlopok furcsán ismétlődnek.',
    'img_64a6aa33c2.jpg': 'Az épületen látható feliratok — beleértve a kapu feletti szöveget — értelmetlen karakterek, ami AI-képekre jellemző.',
    'img_aeb5191874.jpg': 'A szoba túlzottan rendes és szimmetrikus, minden növény tökéletes elrendezésben áll — valódi szobafotókon mindig látszik rendetlenség.',
    'img_e7fb2f8a99.jpg': 'A férfi kezében látható telefon furcsán pozicionált, és az árnyékok iránya nem felel meg a képen látható napfény irányának.',
    'img_14ea3811bf.jpg': 'A tűzcsap formája rendkívül szimmetrikus és középre helyezett, a háttérkép pedig túlságosan elmosódott — ez AI-ra jellemző.',
    'img_84cab7b3fe.jpg': 'A plüssállatok között elhelyezkedő kis figura alakja deformált és nem azonosítható állatként, fizikailag is lehetetlen a pozíciója.',
    'img_9414c7852c.jpg': 'A forgalom iránya és az útjelző táblák egy része fizikailag lehetetlen elrendezést mutat, a piros fény nyomvonalak szimmetrikusak.',
    'img_f929d8aaf5.jpg': 'A motokrossz motorokon látható számok és betűk a matricákon olvashatatlanok és értelmetlenek — tipikus AI-hiba.',
    'img_4c7e8f6fd7.jpg': 'A pizza üzlet felirata a képen többször ismétlődik érthetetlen módon, a motoros sisakok simaak és arcvonal nélküliek.',
    'img_272439ebf6.jpg': 'A visszapillantó tükörben látható motoros felső teste és a motor fizikailag nem illik össze, a kerekek elmosódottan látszanak.',
    'img_8b57fb1d1a.jpg': 'A könyvek gerince a polcokon olvashatatlan és értelmetlen — az AI nem tud olvasható könyvcímeket generálni.',
    'img_e648d2c090.jpg': 'A kép stílusa részben rajzfilm-szerű, a feliratok értelmetlen karaktersorozatokból állnak — egyértelmű AI-generálás.',
    'img_f814fcadf2.jpg': 'A monitorok képernyői teljesen feketék, a kamerán a felirat olvashatatlan, az arcok kissé elmosódottak és mesterségesek.',
    'img_ea2b4d70db.jpg': 'A kép stílusa részben rajzfilm-szerű, az útjelző táblák értelmetlen karaktereket tartalmaznak, a város rajzolt textúrával rendelkezik.',
    'img_1daad43a87.jpg': 'A nő kezének ujjai a tál körül furcsán elrendeződtek, a konyhai eszközök pozíciója és az összefüggések nem logikusak.',
    'img_3a167a7895.jpg': 'A férfi latex kesztyűje nem illik a konyhai munkához, és a kötény felirata elmosódott, olvashatatlan karaktereket mutat.',
    'img_3750b79e09.jpg': 'A férfi bőrének textúrája és az arc arányai túl tökéletesek, a haj és szakáll egyenletesebb mint egy valódi személynél.',
    'img_ded62d363f.jpg': 'A tűzcsap teteje szokatlan kupola formájú, ami nem felel meg a valódi tűzcsapok szabványos kialakításának.',
    'img_e88e4c109b.jpg': 'A kőbe gravált feliraton teljesen értelmetlen szöveg látható, ami az AI szöveg-renderelési hibájára utal.',
    'img_92d4a0f486.jpg': 'A porceláncsészén és a kekszen látható minták túl tökéletesek és szimmetrikusak — valódi süteményen és edényen ez ritka.',
    'img_0e9685a1cc.jpg': 'A Colosseum köré modern épületeket és taxikat generált az AI, ami történelmileg és földrajzilag lehetetlen.',
    'img_a2b01800da.jpg': 'A motorkerékpár alkatrészei logikátlanul illeszkednek egymáshoz, a füst elrendezése mesterségesen szimmetrikus.',
    'img_93a6d23e47.jpg': 'Az állomásépület és a sínen látható felirat elmosódott és olvashatatlan, a felső huzalrendszer nem konzisztens a valósággal.',
    'img_a1154701fd.jpg': 'A juhok szőrének textúrája túl egyszerű és sima, az egyik juh lábai furcsa szögben állnak, a sziklafal textúrája sem következetes.',
    'img_401f4ea00e.jpg': 'A parkolóvonalak és rendszámok teljesen olvashatatlanok, az autók arányai és a visszapillantók nem szabványosak.',
    'img_c4878bae7f.jpg': 'A férfi bal kezének ujjai furcsán hajlanak a telefon körül, és a jobb kezében tartott második készülék a levegőben lebeg.',
    'img_8d33c1f457.jpg': 'A két vonat túl szimmetrikus és azonos a színezetében, a sínpálya és az állomás geometriája sem következetes valódi felvétellel.',
    'img_962f563014.jpg': 'A kép egyértelmű rajzfilm-stílusú — a busz és a környezet nem fotó, hanem AI által generált illusztráció.',
    'img_063c14efde.jpg': 'Az utcanévtáblákon teljesen értelmetlen és olvashatatlan szöveg látható, ami az AI tipikus szöveg-renderelési hibája.',
    'img_220ab83781.jpg': 'A motor matricáinak feliratai olvashatatlanok, a háttér útfelszíne és kerítései elmosódottan egybemosódnak.',
    'img_878465b260.jpg': 'A kép akvarell- vagy olajfestmény-jellegű, nem fotó — az emberek és járművek rajzolt megjelenésűek.',
    'img_3c5b0d1652.jpg': 'A plüssmedve a motoron fizikailag nem tartható meg, és a motor kerekei és a kabát részletei következetlenek.',
    'img_6bd7b0f907.jpg': 'A kis zsiráfborjú aránytalanul kicsi a felnőtt zsiráfhoz képest, a csoport elhelyezése és az állatok pozíciói nem következetesek.',
    'img_4f9a168467.jpg': 'Az asztalon két különböző billentyűzet egymáson fekszik logikátlanul, az Apple iMac mellé nem illik az összes többi eszköz stílusa.',
    'img_3442eb1de3.jpg': 'A két szakács arca túl szimmetrikus és sima bőrrel rendelkezik, a háttér polcok túl egyenletesek és valószerűtlenek.',
    'img_716e56dd1f.jpg': 'A padon ülők fejei és kalapjai túl szimmetrikusak, és a hajukon látható textúra mesterséges előállítást mutat.',
    'img_14db25e42b.jpg': 'A konyha túl tökéletesen rendes és szimmetrikus, a polcokon lévő edények mintái olvashatatlanok, a padló kockamintája torzul a sarkoknál.',
    'img_5c2192cfd2.jpg': 'A felvonulási kocsi tábláján olvashatatlan karakterekből álló felirat látható, a tömeg arckifejezése egyformább mint valódi felvételen.',
    'img_94d328683c.jpg': 'A híd szerkezete fizikailag nem működőképes — a tartók szimmetrikusak, de a megtámasztás nem következetes.',
    'img_b57367150f.jpg': 'A fogkefe-tartóban lévő fogkefék száma és elrendezése furcsa, a virágszirmok túl tökéletesek és szimmetrikusak.',
    'img_401abf6558.jpg': 'A jobb felső sarokban látható "2r" felirat értelmetlenül elhelyezett, és a WC-tartály csővezetéke fizikailag nem logikus.',
}

idx_by_file = {e['file'].split('/')[-1]: i for i, e in enumerate(manifest)}

updated = 0
for fname, expl in explanations.items():
    idx = idx_by_file.get(fname)
    if idx is not None:
        manifest[idx]['explanation'] = expl
        updated += 1

with open('images.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f'Frissítve: {updated} magyarázat')
