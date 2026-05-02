"""
Demo kullanici ve gercekci puan seed scripti.
Calistirmak icin: python -X utf8 seed/seed_demo_ratings.py

Amac:
- 3 demo kullanici olusturur (yoksa).
- Her demo kullanici, tum 75 icerigi "izlemis" ve puanlamis gibi KullaniciProgram'a eklenir.
- AFTER INSERT/UPDATE triggeri Program.ortalama_puan'i otomatik gunceller.
- Boylece min-puan filtresi ve oneri siralamalari gercekci calisir.

Puanlama mantigi:
- Hedef puan (TARGET_RATINGS): gercek hayattaki izleyici algisini yansitir.
- 3 kullanici ayni icerigi hafifce farkli puanlar: +0.5 / 0.0 / -0.5 offset.
- Birlikte ortalama ~= hedef puana yakinsar.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import db
from utils.password_hasher import hash_password
from datetime import date

# ─── Hedef ortalama puanlar ──────────────────────────────────────────────────
# (izleyici algisina dayali demo degerler — resmi bir kaynaktan alinmamistir)
TARGET_RATINGS = {
    # Tier 1 — 9.0  (Ikonik, cok begenilen)
    "Kara Sovalye":                          9.0,
    "Baslangic":                             9.0,
    "Interstellar":                          9.0,
    "Yuzuklerin Efendisi: Iki Kule":         9.0,
    "Yuzuklerin Efendisi: Kralin Donusu":    9.0,
    "Dangal":                                9.0,
    "Bizi Hatirla":                          9.0,
    "Stranger Things":                       9.0,

    # Tier 2 — 8.5  (Cok iyi, genis kitleye hitap eden)
    "Jurassic Park":                         8.5,
    "Shrek":                                 8.5,
    "Gezegenimiz":                           8.5,
    "How I Met Your Mother":                 8.5,
    "The Blacklist":                         8.5,

    # Tier 3 — 8.0  (Iyi, basarili)
    "Harry Potter: Olum Yadigarlari":        8.0,
    "PK":                                    8.0,
    "Mercan Pesinde":                        8.0,
    "Kung Fu Panda":                         8.0,
    "Jaws":                                  8.0,
    "Dirilis Ertugrul":                      8.0,
    "Leyla ile Mecnun":                      8.0,
    "Masa ve Koca Ayi":                      8.0,

    # Tier 4 — 7.5  (Ortanin ustu)
    "Sherlock Holmes":                       7.5,
    "Fantastik Canavarlar":                  7.5,
    "Mission Blue":                          7.5,
    "Plastik Okyanus":                       7.5,
    "Mega Zeka":                             7.5,
    "Yercekimi":                             7.5,
    "Ejderhalar":                            7.5,
    "Trol Avcilari: Arcadia Hikayeleri":     7.5,
    "The Originals":                         7.5,
    "Sunger Bob":                            7.5,
    "Criminal":                              7.5,
    "Gezegenimiz: Ozel Bolum":               7.5,
    "Orumcek Adam":                          7.5,
    "Dunyanin En Sira Disi Evleri":          7.5,
    "Basketball or Nothing":                 7.5,

    # Tier 5 — 7.0  (Iyi ama ayirt edici degil)
    "Maske":                                 7.0,
    "Jurassic World":                        7.0,
    "Kuslarla Dans":                         7.0,
    "Ay'daki Son Adam":                      7.0,
    "Ben Efsaneyim":                         7.0,
    "Pokemon: Dedektif Pikachu":             7.0,
    "Charlie'nin Cikolata Fabrikasi":        7.0,
    "Mr. Bean Tatilde":                      7.0,
    "Da Vinci Sifresi":                      7.0,
    "Atiye":                                 7.0,
    "Kuscular":                              7.0,
    "Marsta Kesif":                          7.0,
    "Car Masters":                           7.0,
    "Buyuk Tasarimlar":                      7.0,
    "Siradixi Kulupler":                     7.0,

    # Tier 6 — 6.5  (Orta)
    "Dream Big":                             6.5,
    "Rakamlarla Tahmin":                     6.5,
    "72 Sevimli Hayvan":                     6.5,
    "Pandemic":                              6.5,
    "Kardesim Benim":                        6.5,
    "Beni Boyle Sev":                        6.5,
    "Patron Bebek Yine Is Basinda":          6.5,
    "Beyblade":                              6.5,
    "Sonic X":                               6.5,
    "Kung Fu Panda: Muhtesem Sirlar":        6.5,
    "The Big Family Cooking":                6.5,

    # Tier 7 — 6.0  (Altorta)
    "Scooby-Doo":                            6.0,
    "Angry Birds":                           6.0,
    "Frankenstein":                          6.0,
    "Delibal":                               6.0,

    # Tier 8 — 5.5 / 5.0  (Zayif veya tartismali)
    "Recep Ivedik 6":                        5.5,
    "Assassin's Creed":                      5.5,
    "Alaca Karanlik":                        5.5,
    "Ninja Kaplumbagalar":                   5.5,
    "Arif V 216":                            5.5,
    "Sirinler":                              5.5,
    "Alvin ve Sincaplar":                    5.5,
    "Marvel Iron Fist":                      5.5,
    "Transformers: Kayip Cag":               5.0,
}

# ─── Demo kullanicilar ───────────────────────────────────────────────────────
DEMO_USERS = [
    {
        "ad": "Ali",    "soyad": "Yilmaz",
        "email": "ali.yilmaz@demo.test",
        "cinsiyet": "Erkek", "offset": +0.5,
    },
    {
        "ad": "Ayse",   "soyad": "Kaya",
        "email": "ayse.kaya@demo.test",
        "cinsiyet": "Kadin", "offset":  0.0,
    },
    {
        "ad": "Mehmet", "soyad": "Demir",
        "email": "mehmet.demir@demo.test",
        "cinsiyet": "Erkek", "offset": -0.5,
    },
]
_DEMO_SIFRE = "Demo1234!"


def _user_puan(target: float, offset: float) -> int:
    return max(1, min(10, round(target + offset)))


def run():
    print("=" * 58)
    print("  Demo Rating Seed Basladi")
    print("=" * 58)

    # 1. Demo kullanicilari olustur (yoksa)
    print("\n[1] Demo kullanicilar kontrol ediliyor...")
    user_ids = []
    sifre_hash = hash_password(_DEMO_SIFRE)
    for u in DEMO_USERS:
        existing = db.fetchone(
            "SELECT kullanici_id FROM Kullanici WHERE email = ?",
            (u["email"],)
        )
        if existing:
            uid = existing[0]
            print(f"    Zaten var : {u['email']} (id={uid})")
        else:
            uid = db.insert_and_get_id(
                "INSERT INTO Kullanici "
                "(ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id) "
                "OUTPUT INSERTED.kullanici_id VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (u["ad"], u["soyad"], u["email"], sifre_hash,
                 date(1990, 1, 1), u["cinsiyet"], "Turkiye", 1)
            )
            print(f"    + Olusturuldu: {u['email']} (id={uid})")
        user_ids.append((uid, u["offset"]))

    # 2. Program id + bolum/sure bilgilerini toplu al
    print("\n[2] Program bilgileri aliniyor...")
    all_programs = db.fetchall(
        "SELECT program_id, ad, bolum_sayisi, bolum_suresi FROM Program"
    )
    program_map = {row[1]: {"pid": row[0], "bolum": row[2] or 1,
                             "sure": row[3] or 60}
                   for row in all_programs}

    missing = [ad for ad in TARGET_RATINGS if ad not in program_map]
    if missing:
        print(f"    UYARI — Asagidaki programlar DB'de bulunamadi:")
        for m in missing:
            print(f"      - {m}")
    found = len(TARGET_RATINGS) - len(missing)
    print(f"    {found} / {len(TARGET_RATINGS)} program eslesti.")

    # 3. KullaniciProgram kayitlarini ekle / guncelle
    print("\n[3] Demo puanlar isleniyor...")
    eklenen = guncellenen = atlanan = 0

    for ad, target in TARGET_RATINGS.items():
        if ad not in program_map:
            continue
        prog  = program_map[ad]
        pid   = prog["pid"]
        bolum = prog["bolum"]
        sure  = prog["sure"]

        for uid, offset in user_ids:
            puan = _user_puan(target, offset)
            existing = db.fetchone(
                "SELECT puan FROM KullaniciProgram "
                "WHERE kullanici_id = ? AND program_id = ?",
                (uid, pid)
            )
            if existing is None:
                db.execute(
                    "INSERT INTO KullaniciProgram "
                    "(kullanici_id, program_id, son_bolum, son_dakika, tamamlandi, puan) "
                    "VALUES (?, ?, ?, ?, 1, ?)",
                    (uid, pid, bolum, sure, puan)
                )
                eklenen += 1
            elif existing[0] != puan:
                db.execute(
                    "UPDATE KullaniciProgram SET puan = ? "
                    "WHERE kullanici_id = ? AND program_id = ?",
                    (puan, uid, pid)
                )
                guncellenen += 1
            else:
                atlanan += 1

    print(f"    Eklendi    : {eklenen}")
    print(f"    Guncellendi: {guncellenen}")
    print(f"    Zaten dogru: {atlanan}")

    # 4. Sonuc ozeti
    row = db.fetchone(
        "SELECT COUNT(*) FROM Program WHERE ortalama_puan > 0"
    )
    print(f"\n[4] ortalama_puan > 0 olan program sayisi: {row[0]}")

    # En yuksek 5 puan ornegi
    top5 = db.fetchall(
        "SELECT TOP 5 ad, ortalama_puan FROM Program "
        "WHERE ortalama_puan > 0 ORDER BY ortalama_puan DESC"
    )
    if top5:
        print("    En yuksek 5 puan:")
        for ad, puan in top5:
            print(f"      {puan:.2f}  {ad}")

    print("\n  Demo rating seed tamamlandi!")
    print("=" * 58)


if __name__ == "__main__":
    run()
