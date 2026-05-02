"""
Netflix DB verilerini veritabanina aktar.
Calistirmak icin: python -X utf8 seed/seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import db

TURLER = [
    "Aksiyon ve Macera", "Bilim Kurgu ve Fantastik Yapimlar", "Bilim Kurgu",
    "Romantik", "Drama", "Belgesel", "Bilim ve Doga", "Cocuk ve Aile",
    "Komedi", "Korku", "Gerilim", "Anime", "Reality Program",
]

# (ad, aciklama, tip, yil, bolum_sayisi, bolum_suresi, [turler])
PROGRAMLAR = [
    # --- FİLMLER ---
    ("Recep Ivedik 6","Recep Ivedik'in yeni maceralari.","Film",2019,1,98,["Aksiyon ve Macera"]),
    ("Assassin's Creed","Tarihi suikastcilarin torununu konu alan aksiyon filmi.","Film",2016,1,115,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Alaca Karanlik","Vampir ask hikayesi.","Film",2008,1,122,["Aksiyon ve Macera","Romantik"]),
    ("Yuzuklerin Efendisi: Iki Kule","Orta Dunya'nin destansi hikayesi devam ediyor.","Film",2002,1,179,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Maske","Buyulu bir maskenin giyen kisiye guc verdigi komedi aksiyon filmi.","Film",1994,1,101,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Kara Sovalye","Batman'in Gotham sehrini Joker'den kurtarma mucadelesi.","Film",2008,1,152,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Sherlock Holmes","Unlu dedektifin yeni bir davay cozduğu aksiyon macerasI.","Film",2009,1,128,["Aksiyon ve Macera"]),
    ("Yuzuklerin Efendisi: Kralin Donusu","Yuzuk Kardesliginin destansi son savasi.","Film",2003,1,201,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Transformers: Kayip Cag","Otobotlar ile Decepticonlar arasindaki savas devam ediyor.","Film",2014,1,165,["Aksiyon ve Macera"]),
    ("Baslangic","Ruya katmanlarinda gecen zihin bukucu bir aksiyon gerilim filmi.","Film",2010,1,148,["Aksiyon ve Macera"]),
    ("Interstellar","Insanligi kurtarmak icin evrenin derinliklerine yolculuk.","Film",2014,1,169,["Aksiyon ve Macera","Drama"]),
    ("Harry Potter: Olum Yadigarlari","Harry Potter serisinin son bolumu.","Film",2010,1,146,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar","Cocuk ve Aile"]),
    ("Jurassic World","Dinozourlarin yeniden canlastigi tema parkinda korku basliyor.","Film",2015,1,124,["Aksiyon ve Macera"]),
    ("Fantastik Canavarlar","Sihirli yaratiklarin dunyasinda gecen buyuleyici macera.","Film",2016,1,133,["Aksiyon ve Macera","Cocuk ve Aile"]),
    ("Ninja Kaplumbagalar","Dort ninja kaplumbaganin sehri koruma mucadelesi.","Film",2014,1,101,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Kuslarla Dans","Kuslarin esiz dans rituelerini konu alan belgesel.","Film",2019,1,96,["Belgesel"]),
    ("Mission Blue","Okyanus bilimcisi Sylvia Earle'in denizleri koruma mucadelesi.","Film",2014,1,95,["Belgesel"]),
    ("Mercan Pesinde","Mercan resiflerinin yok oluşunu anlatan belgesel.","Film",2017,1,89,["Belgesel"]),
    ("Dream Big","Muhendisligin dunyayi nasil sekillendirdigini anlatan belgesel.","Film",2017,1,47,["Belgesel"]),
    ("Ay'daki Son Adam","Apollo 17 gorevinin son Ay yuruyu^cusuunu anlatan belgesel.","Film",2016,1,98,["Belgesel"]),
    ("Plastik Okyanus","Okyanuslardaki plastik kirliligini belgeleyen film.","Film",2016,1,102,["Belgesel"]),
    ("Rakamlarla Tahmin","Veri bilimiyle gelecegi tahmin etme uzerine belgesel.","Film",2018,1,85,["Belgesel"]),
    ("Ben Efsaneyim","Virus sonrasi issiz kalan dunyada hayatta kalan son insanin hikayesi.","Film",2007,1,101,["Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Arif V 216","Turk sinemasinin sevilen karakteri Arif'in yeni macerasI.","Film",2018,1,120,["Bilim Kurgu ve Fantastik Yapimlar","Komedi"]),
    ("PK","Dunyaya dusen uzaylinin insanligi sorgulayan komedi filmi.","Film",2014,1,153,["Bilim Kurgu ve Fantastik Yapimlar","Romantik"]),
    ("Orumcek Adam","Peter Parker'in orumcek isirigindan sonra kahraman olusu.","Film",2002,1,121,["Aksiyon ve Macera","Bilim Kurgu ve Fantastik Yapimlar"]),
    ("Jurassic Park","Dinozourlarin genetik klonlamayla yeniden hayata donduruldugu park.","Film",1993,1,127,["Bilim Kurgu ve Fantastik Yapimlar","Aksiyon ve Macera"]),
    ("Frankenstein","Mary Shelley'nin klasik eserinden uyarlanan korku filmi.","Film",1994,1,123,["Bilim Kurgu ve Fantastik Yapimlar","Aksiyon ve Macera","Korku"]),
    ("Gezegenimiz","Dunyanin dort bir yanindaki dogal guzellikeri anlatan belgesel.","Film",2019,1,90,["Belgesel","Bilim ve Doga"]),
    ("72 Sevimli Hayvan","Dunyanin en sevimli hayvanlarini tanitan eglenceli belgesel.","Film",2017,1,60,["Belgesel","Bilim ve Doga"]),
    ("Kuscular","Kus gozlemcilerinin tutkusunu anlatan belgesel.","Film",2018,1,93,["Belgesel","Bilim ve Doga"]),
    ("Marsta Kesif","Mars'i kesfeden araclarin hikayesini anlatan bilim belgesi.","Film",2016,1,85,["Belgesel","Bilim ve Doga"]),
    ("Gezegenimiz: Ozel Bolum","Gezegenimiz belgeselinin ek icerikleri.","Film",2019,1,45,["Belgesel","Bilim ve Doga"]),
    ("Pandemic","Pandemi hastaliklarına karsi insanligin mucadelesini anlatan belgesel.","Film",2020,1,98,["Belgesel","Bilim ve Doga"]),
    ("Pokemon: Dedektif Pikachu","Pikachu'nun dedektif olarak aktivasyonunu anlatan animasyon.","Film",2019,1,104,["Cocuk ve Aile"]),
    ("Sirinler","Minik mavi yaratiklarin New York'ta yasadigi macerayi anlatan animasyon.","Film",2011,1,103,["Cocuk ve Aile","Komedi"]),
    ("Charlie'nin Cikolata Fabrikasi","Gizemli cikolata fabrikasina kazanan cocuklarin macerasI.","Film",2005,1,115,["Cocuk ve Aile","Komedi"]),
    ("Alvin ve Sincaplar","Muzisyen sincaplarin maceralari.","Film",2007,1,92,["Cocuk ve Aile"]),
    ("Scooby-Doo","Scooby-Doo ve arkadaslarinin canli aksiyon macerasI.","Film",2002,1,86,["Cocuk ve Aile"]),
    ("Kung Fu Panda","Panda Po'nun kung fu ustasi olma hayalini anlatan animasyon.","Film",2008,1,92,["Cocuk ve Aile","Aksiyon ve Macera"]),
    ("Mr. Bean Tatilde","Mr. Bean'in Fransa'da yasadigi komik tatil maceralari.","Film",2007,1,90,["Cocuk ve Aile"]),
    ("Shrek","Yesil devinin prenses kurtarma hikayesi.","Film",2001,1,90,["Cocuk ve Aile","Komedi"]),
    ("Mega Zeka","Kotu oldugu zannedilen super zekalin birinin hikayesi.","Film",2010,1,96,["Cocuk ve Aile","Komedi"]),
    ("Bizi Hatirla","Oluler diyarini ziyaret eden cocugun buyusu.","Film",2017,1,105,["Drama"]),
    ("Delibal","Bir ask hikayesinin duygu yuklu anlatimiI.","Film",2015,1,102,["Drama","Romantik"]),
    ("Kardesim Benim","Iki kardesin komik ve duygusal hikayesi.","Film",2016,1,108,["Drama","Komedi"]),
    ("Dangal","Hint gures sampiyonluguna giden bir babanin kizlariyla hikayesi.","Film",2016,1,161,["Drama"]),
    ("Yercekimi","Uzayda mahsur kalan astronotlarin hayatta kalma mucadelesi.","Film",2013,1,91,["Bilim Kurgu","Drama"]),
    ("Jaws","Kucuk bir kasabay kaplayan dev kopekbaligi tehdidi.","Film",1975,1,124,["Gerilim"]),
    ("Da Vinci Sifresi","Louvre'daki cinayeti cozmeye calisan profesorun gizemli yolculugu.","Film",2006,1,149,["Gerilim"]),
    # --- DİZİLER ---
    ("Marvel Iron Fist","Dobus sanatlarinda usta bir super kahramanin New York'u korumasi.","Dizi",2017,26,55,["Aksiyon ve Macera"]),
    ("Ejderhalar","Hiccup ve ejderhasi Toothless'in animasyon macerasI.","Dizi",2012,117,22,["Cocuk ve Aile","Aksiyon ve Macera"]),
    ("Dirilis Ertugrul","Osmanli Imparatorlugu'nun kurulusuna giden destansi Turk dizisi.","Dizi",2014,150,120,["Aksiyon ve Macera"]),
    ("Trol Avcilari: Arcadia Hikayeleri","Yuzeyinin altindaki trol dunyasini kesfeden cocuklarin macerasI.","Dizi",2016,52,24,["Cocuk ve Aile","Aksiyon ve Macera"]),
    ("How I Met Your Mother","Bir babanin cocuklarına annesini nasil tanidiginI anlattiği komedi dizisi.","Dizi",2005,208,22,["Romantik"]),
    ("Leyla ile Mecnun","Turk yapimi absurd komedi ve romantik dizi.","Dizi",2011,75,50,["Romantik"]),
    ("Beni Boyle Sev","Iki zit karakterin ask hikayesini anlatan Turk romantik dramasi.","Dizi",2009,136,120,["Drama","Romantik"]),
    ("Patron Bebek Yine Is Basinda","Patron Bebegin animasyon maceralarinin devami.","Dizi",2018,78,22,["Cocuk ve Aile","Komedi"]),
    ("Atiye","Antik semboller etrafinda donen mistik Turk gerilim dizisi.","Dizi",2019,24,45,["Aksiyon ve Macera","Romantik"]),
    ("Masa ve Koca Ayi","Merakli kiz cocugu Masa ile buyuk ayinin maceralari.","Dizi",2009,78,7,["Cocuk ve Aile"]),
    ("Sunger Bob","Bikini Bottom'da yasayan sungenin komik gunluk maceralari.","Dizi",1999,284,11,["Cocuk ve Aile","Komedi"]),
    ("Stranger Things","Kucuk bir kasabada gizemli olaylar yasayan cocuklarin aksiyon/korku hikayesi.","Dizi",2016,34,50,["Aksiyon ve Macera","Korku"]),
    ("The Originals","Ilk vampir ailesinin New Orleans'ta guc mucadelesi.","Dizi",2013,92,42,["Drama","Korku"]),
    ("Angry Birds","Ofkeli kuslarin animasyon seruuveni.","Dizi",2013,104,3,["Cocuk ve Aile","Komedi"]),
    ("Criminal","Farkli ulkelerde gecen sorgu odasi gerilim antoloji dizisi.","Dizi",2019,16,45,["Gerilim"]),
    ("Beyblade","Donduren topac dovuslerine dayali anime serisi.","Dizi",2001,51,22,["Anime","Cocuk ve Aile"]),
    ("Sonic X","Hiz kahramani Sonic'in maceralarini anlatan anime.","Dizi",2003,78,22,["Anime","Aksiyon ve Macera"]),
    ("Kung Fu Panda: Muhtesem Sirlar","Kung Fu Panda filminin animasyon spin-off dizisi.","Dizi",2018,26,22,["Aksiyon ve Macera"]),
    ("The Blacklist","FBI'in en cok aranan suclusunun ajanlarla isbirligi yapmasinin gerilim dizisi.","Dizi",2013,159,43,["Aksiyon ve Macera","Gerilim"]),
    # --- TV SHOW ---
    ("Dunyanin En Sira Disi Evleri","Dunyanin farkli koselerindeki alisilagelmis yasam alanlarina yolculuk.","Tv Show",2018,26,30,["Reality Program"]),
    ("Car Masters","Klasik arabalari restore eden ustalar.","Tv Show",2018,24,45,["Reality Program"]),
    ("Buyuk Tasarimlar","Mimar ve tasarimcilarin yaratici projelerini anlatan program.","Tv Show",2019,18,40,["Reality Program"]),
    ("Basketball or Nothing","Navajo genclerinin basket yolculugunu anlatan gerceklik programi.","Tv Show",2019,6,35,["Reality Program"]),
    ("The Big Family Cooking","Ailelerle gerceklestirilen buyuk yemek yarismasI.","Tv Show",2017,8,45,["Reality Program"]),
    ("Siradixi Kulupler","Dunyanin en tuhaf ve ilginc kuluiplerini kesfeden program.","Tv Show",2019,12,30,["Reality Program"]),
]


def run():
    print("=" * 50)
    print("  Seed Data Aktarimi Basladi")
    print("=" * 50)

    # 1. Türleri ekle
    print("\n[1] Turler ekleniyor...")
    tur_id_map = {}
    for tur_adi in TURLER:
        existing = db.fetchone("SELECT tur_id FROM Tur WHERE tur_adi = ?", (tur_adi,))
        if existing:
            tur_id_map[tur_adi] = existing[0]
            print(f"    Zaten var: {tur_adi}")
        else:
            new_id = db.insert_and_get_id(
                "INSERT INTO Tur (tur_adi) OUTPUT INSERTED.tur_id VALUES (?)",
                (tur_adi,)
            )
            tur_id_map[tur_adi] = new_id
            print(f"    + {tur_adi} (id={new_id})")

    # 2. Programları ekle
    print(f"\n[2] {len(PROGRAMLAR)} program ekleniyor...")
    eklenen = 0
    atlanan = 0
    for p in PROGRAMLAR:
        ad, aciklama, tip, yil, bolum, sure, turler = p
        existing = db.fetchone("SELECT program_id FROM Program WHERE ad = ?", (ad,))
        if existing:
            atlanan += 1
            pid = existing[0]
        else:
            pid = db.insert_and_get_id(
                "INSERT INTO Program (ad, aciklama, program_tipi, yayin_yili, "
                "bolum_sayisi, bolum_suresi) OUTPUT INSERTED.program_id "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (ad, aciklama, tip, yil, bolum, sure)
            )
            eklenen += 1

        # Türleri bağla
        for tur_adi in turler:
            tid = tur_id_map.get(tur_adi)
            if tid:
                exists = db.fetchone(
                    "SELECT 1 FROM ProgramTur WHERE program_id=? AND tur_id=?",
                    (pid, tid)
                )
                if not exists:
                    db.execute(
                        "INSERT INTO ProgramTur (program_id, tur_id) VALUES (?, ?)",
                        (pid, tid)
                    )

    print(f"    Eklendi: {eklenen}, Zaten vardi: {atlanan}")

    # 3. Kontrol
    row = db.fetchone("SELECT COUNT(*) FROM Program")
    tur_row = db.fetchone("SELECT COUNT(*) FROM Tur")
    print(f"\n[3] Sonuc:")
    print(f"    Program sayisi: {row[0]}")
    print(f"    Tur sayisi:     {tur_row[0]}")
    print("\n  Seed data tamamlandi!")
    print("=" * 50)


if __name__ == "__main__":
    run()
