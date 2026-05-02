"""
Veritabani kurulum scripti.
Calistirmak icin: py -3.12 database/setup.py
"""

import os
import sys

import pyodbc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DB_CONFIG


def _iter_connection_strings(database_name: str):
    preferred_drivers = [
        DB_CONFIG.get("driver"),
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "SQL Server",
    ]
    seen = set()

    for driver in preferred_drivers:
        if not driver or driver in seen:
            continue
        seen.add(driver)

        parts = [
            f"DRIVER={{{driver}}}",
            f"SERVER={DB_CONFIG['server']}",
            f"DATABASE={database_name}",
            f"Trusted_Connection={DB_CONFIG.get('trusted_connection', 'yes')}",
        ]

        if "ODBC Driver" in driver:
            parts.extend(["Encrypt=no", "TrustServerCertificate=yes"])

        yield driver, ";".join(parts) + ";"


def open_connection(database_name: str, autocommit: bool = False):
    errors = []

    for driver, conn_str in _iter_connection_strings(database_name):
        try:
            conn = pyodbc.connect(conn_str, autocommit=autocommit)
            return conn, driver
        except pyodbc.Error as exc:
            errors.append(f"{driver}: {exc}")

    raise RuntimeError(
        "SQL Server baglantisi kurulamadi.\n" + "\n".join(errors)
    )


def split_sql_batches(sql_text: str):
    batches = []
    current = []

    for line in sql_text.splitlines():
        if line.strip().upper() == "GO":
            batch = "\n".join(current).strip()
            if batch:
                batches.append(batch)
            current = []
            continue
        current.append(line)

    batch = "\n".join(current).strip()
    if batch:
        batches.append(batch)

    return batches


def ensure_database_exists():
    """Veritabani yoksa master uzerinden olusturur."""
    conn, driver = open_connection("master", autocommit=True)
    try:
        cursor = conn.cursor()
        row = cursor.execute(
            "SELECT DB_ID(?)",
            (DB_CONFIG["database"],),
        ).fetchone()

        if row and row[0] is not None:
            print(
                f"    Veritabani zaten var: {DB_CONFIG['database']} ({driver})"
            )
            return

        cursor.execute(f"CREATE DATABASE [{DB_CONFIG['database']}]")
        print(
            f"    Veritabani olusturuldu: {DB_CONFIG['database']} ({driver})"
        )
    finally:
        conn.close()


def run_sql_file(sql_path):
    """SQL dosyasini pyodbc ile batch batch calistirir."""
    with open(sql_path, "r", encoding="utf-8", errors="replace") as file:
        sql_text = file.read()

    conn, driver = open_connection(DB_CONFIG["database"], autocommit=True)
    try:
        cursor = conn.cursor()
        for index, batch in enumerate(split_sql_batches(sql_text), start=1):
            try:
                cursor.execute(batch)
            except pyodbc.Error as exc:
                print(f"    [HATA] Batch {index}: {exc}")
                return False
        print(f"    SQL dosyasi basariyla calistirildi ({driver}).")
        return True
    finally:
        conn.close()


def seed_roles_and_admin():
    from database.connection import db
    import bcrypt

    print("\n[3] Roller ekleniyor...")
    for rol in [("kullanici",), ("yonetici",)]:
        existing = db.fetchone("SELECT rol_id FROM Rol WHERE rol_adi = ?", rol)
        if not existing:
            db.execute("INSERT INTO Rol (rol_adi) VALUES (?)", rol)
            print(f"    + {rol[0]}")
        else:
            print(f"    Zaten var: {rol[0]}")

    print("\n[4] Yonetici hesabi kontrol ediliyor...")
    existing = db.fetchone(
        "SELECT kullanici_id FROM Kullanici WHERE email = ?",
        ("admin@netflix.com",),
    )
    if not existing:
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        db.execute(
            """INSERT INTO Kullanici
               (ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "Admin",
                "Netflix",
                "admin@netflix.com",
                hashed,
                "1990-01-01",
                "Diger",
                "Turkiye",
                2,
            ),
        )
        print("    Yonetici olusturuldu >> admin@netflix.com / admin123")
    else:
        print("    Yonetici zaten mevcut.")


def verify_tables():
    from database.connection import db

    print("\n[5] Tablo kontrolu...")
    tables = [
        "Rol",
        "Kullanici",
        "Tur",
        "KullaniciTur",
        "Program",
        "ProgramTur",
        "Bolum",
        "KullaniciProgram",
        "Favori",
        "OturumLog",
        "IzlemeLog",
    ]
    all_ok = True
    for table in tables:
        row = db.fetchone(
            "SELECT COUNT(*) FROM sys.tables WHERE name = ?",
            (table,),
        )
        ok = row and row[0] == 1
        if not ok:
            all_ok = False
        print(f"    [{'OK' if ok else 'EKSIK'}] {table}")
    return all_ok


if __name__ == "__main__":
    print("=" * 52)
    print("   Netflix Platform - Veritabani Kurulumu")
    print("=" * 52)

    sql_path = os.path.join(
        os.path.dirname(__file__), "migrations", "001_create_tables.sql"
    )

    print("\n[1] Veritabani kontrol ediliyor...")
    ensure_database_exists()

    print("\n[2] Tablolar olusturuluyor...")
    success = run_sql_file(sql_path)
    if success:
        print("    Tablolar hazir.")
    else:
        print("    SQL dosyasi calistirilirken hata olustu.")

    seed_roles_and_admin()
    ok = verify_tables()

    print("\n" + "=" * 52)
    if ok:
        print("   Kurulum TAMAMLANDI! Tum tablolar hazir.")
    else:
        print("   UYARI: Bazi tablolar eksik olabilir.")
    print("=" * 52)
