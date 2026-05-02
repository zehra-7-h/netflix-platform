"""
Veritabanı kurulum scripti.
Çalıştırmak için: python database/setup.py
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_sql_file(sql_path):
    """SQL dosyasını sqlcmd ile çalıştırır (GO ifadelerini destekler)."""
    result = subprocess.run(
        ["sqlcmd", "-S", r".\SQLEXPRESS", "-d", "netflix_db",
         "-i", sql_path, "-b"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    output = (result.stdout or "") + (result.stderr or "")
    for line in output.splitlines():
        line = line.strip()
        if line and not line.startswith("---"):
            try:
                print(f"    {line}")
            except UnicodeEncodeError:
                print(f"    [sqlcmd ciktisi]")
    return result.returncode == 0


def seed_roles_and_admin():
    from database.connection import db
    import bcrypt

    print("\n[2] Roller ekleniyor...")
    for rol in [("kullanici",), ("yonetici",)]:
        existing = db.fetchone("SELECT rol_id FROM Rol WHERE rol_adi = ?", rol)
        if not existing:
            db.execute("INSERT INTO Rol (rol_adi) VALUES (?)", rol)
            print(f"    + {rol[0]}")
        else:
            print(f"    Zaten var: {rol[0]}")

    print("\n[3] Yönetici hesabı kontrol ediliyor...")
    existing = db.fetchone(
        "SELECT kullanici_id FROM Kullanici WHERE email = ?",
        ("admin@netflix.com",)
    )
    if not existing:
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        db.execute(
            """INSERT INTO Kullanici
               (ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ("Admin", "Netflix", "admin@netflix.com", hashed,
             "1990-01-01", "Diger", "Turkiye", 2)
        )
        print("    Yonetici olusturuldu >> admin@netflix.com / admin123")
    else:
        print("    Yönetici zaten mevcut.")


def verify_tables():
    from database.connection import db
    print("\n[4] Tablo kontrolü...")
    tables = ["Rol", "Kullanici", "Tur", "KullaniciTur", "Program",
              "ProgramTur", "Bolum", "KullaniciProgram", "Favori",
              "OturumLog", "IzlemeLog"]
    all_ok = True
    for table in tables:
        row = db.fetchone(
            "SELECT COUNT(*) FROM sys.tables WHERE name = ?", (table,)
        )
        ok = row and row[0] == 1
        if not ok:
            all_ok = False
        print(f"    [{'OK' if ok else 'EKSIK'}] {table}")
    return all_ok


if __name__ == "__main__":
    print("=" * 52)
    print("   Netflix Platform — Veritabani Kurulumu")
    print("=" * 52)

    sql_path = os.path.join(
        os.path.dirname(__file__), "migrations", "001_create_tables.sql"
    )

    print("\n[1] Tablolar olusturuluyor...")
    success = run_sql_file(sql_path)
    if success:
        print("    SQL dosyasi basariyla calistirildi.")
    else:
        print("    SQL dosyasi calistirildi (bazi satirlar zaten mevcuttu).")

    seed_roles_and_admin()
    ok = verify_tables()

    print("\n" + "=" * 52)
    if ok:
        print("   Kurulum TAMAMLANDI! Tum tablolar hazir.")
    else:
        print("   UYARI: Bazi tablolar eksik olabilir.")
    print("=" * 52)
