from database.connection import db
from typing import List, Dict


class ReportRepository:

    def top_watched(self, limit: int = 10) -> List[Dict]:
        rows = db.fetchall(
            "SELECT TOP (?) p.ad, p.program_tipi, p.toplam_izlenme, "
            "p.ortalama_puan FROM Program p "
            "ORDER BY p.toplam_izlenme DESC", (limit,)
        )
        return [{"ad": r[0], "tip": r[1],
                 "izlenme": r[2], "puan": float(r[3] or 0)} for r in rows]

    def top_rated(self, limit: int = 10) -> List[Dict]:
        rows = db.fetchall(
            "SELECT TOP (?) p.ad, p.program_tipi, p.ortalama_puan, "
            "p.toplam_izlenme FROM Program p WHERE p.ortalama_puan > 0 "
            "ORDER BY p.ortalama_puan DESC", (limit,)
        )
        return [{"ad": r[0], "tip": r[1],
                 "puan": float(r[2] or 0), "izlenme": r[3]} for r in rows]

    def top_genres(self) -> List[Dict]:
        rows = db.fetchall(
            "SELECT t.tur_adi, SUM(p.toplam_izlenme) AS toplam "
            "FROM Tur t "
            "JOIN ProgramTur pt ON t.tur_id = pt.tur_id "
            "JOIN Program p ON pt.program_id = p.program_id "
            "GROUP BY t.tur_id, t.tur_adi "
            "ORDER BY toplam DESC"
        )
        return [{"tur": r[0], "izlenme": r[1] or 0} for r in rows]

    def most_active_users(self, limit: int = 10) -> List[Dict]:
        rows = db.fetchall(
            "SELECT TOP (?) k.ad + ' ' + k.soyad, k.email, "
            "COUNT(DISTINCT kp.program_id), "
            "COALESCE(SUM(il.izleme_suresi), 0) "
            "FROM Kullanici k "
            "LEFT JOIN KullaniciProgram kp ON k.kullanici_id = kp.kullanici_id "
            "LEFT JOIN IzlemeLog il ON k.kullanici_id = il.kullanici_id "
            "WHERE k.rol_id = 1 "
            "GROUP BY k.kullanici_id, k.ad, k.soyad, k.email "
            "ORDER BY COALESCE(SUM(il.izleme_suresi), 0) DESC", (limit,)
        )
        return [{"isim": r[0], "email": r[1],
                 "icerik_sayisi": r[2], "toplam_dakika": r[3]} for r in rows]

    def last_7_days(self) -> List[Dict]:
        rows = db.fetchall(
            "SELECT p.ad, p.program_tipi, COUNT(*) AS izlenme, "
            "MAX(il.izleme_tarihi) AS son "
            "FROM IzlemeLog il "
            "JOIN Program p ON il.program_id = p.program_id "
            "WHERE il.izleme_tarihi >= DATEADD(day, -7, GETDATE()) "
            "GROUP BY p.program_id, p.ad, p.program_tipi "
            "ORDER BY izlenme DESC"
        )
        return [{"ad": r[0], "tip": r[1],
                 "izlenme": r[2], "son": r[3]} for r in rows]

    def summary(self) -> Dict:
        row = db.fetchone(
            "SELECT "
            "(SELECT COUNT(*) FROM Kullanici WHERE rol_id=1 AND aktif=1), "
            "(SELECT COUNT(*) FROM IzlemeLog), "
            "(SELECT COUNT(*) FROM KullaniciProgram WHERE puan IS NOT NULL), "
            "(SELECT COUNT(*) FROM Program)"
        )
        return {
            "kullanici_sayisi": row[0] or 0,
            "toplam_izlenme": row[1] or 0,
            "toplam_puan": row[2] or 0,
            "toplam_icerik": row[3] or 0,
        }
