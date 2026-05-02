from database.connection import db
from models.user import User
from typing import Optional, List


class UserRepository:

    def find_by_email(self, email: str) -> Optional[User]:
        row = db.fetchone(
            "SELECT kullanici_id, ad, soyad, email, sifre_hash, "
            "dogum_tarihi, cinsiyet, ulke, rol_id, aktif, kayit_tarihi "
            "FROM Kullanici WHERE email = ?", (email,)
        )
        return self._to_user(row) if row else None

    def find_by_id(self, kullanici_id: int) -> Optional[User]:
        row = db.fetchone(
            "SELECT kullanici_id, ad, soyad, email, sifre_hash, "
            "dogum_tarihi, cinsiyet, ulke, rol_id, aktif, kayit_tarihi "
            "FROM Kullanici WHERE kullanici_id = ?", (kullanici_id,)
        )
        return self._to_user(row) if row else None

    def create(self, ad, soyad, email, sifre_hash,
               dogum_tarihi, cinsiyet, ulke, rol_id=1) -> int:
        return db.insert_and_get_id(
            "INSERT INTO Kullanici "
            "(ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id) "
            "OUTPUT INSERTED.kullanici_id "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id)
        )

    def update_profile(self, kullanici_id: int, ad: str, soyad: str,
                       dogum_tarihi, cinsiyet: str, ulke: str):
        db.execute(
            "UPDATE Kullanici SET ad=?, soyad=?, dogum_tarihi=?, "
            "cinsiyet=?, ulke=? WHERE kullanici_id=?",
            (ad, soyad, dogum_tarihi, cinsiyet, ulke, kullanici_id)
        )

    def update_password(self, kullanici_id: int, sifre_hash: str):
        db.execute(
            "UPDATE Kullanici SET sifre_hash=? WHERE kullanici_id=?",
            (sifre_hash, kullanici_id)
        )

    def set_active(self, kullanici_id: int, aktif: bool):
        db.execute(
            "UPDATE Kullanici SET aktif=? WHERE kullanici_id=?",
            (1 if aktif else 0, kullanici_id)
        )

    def get_all_users(self) -> List[User]:
        rows = db.fetchall(
            "SELECT kullanici_id, ad, soyad, email, sifre_hash, "
            "dogum_tarihi, cinsiyet, ulke, rol_id, aktif, kayit_tarihi "
            "FROM Kullanici WHERE rol_id = 1 ORDER BY kayit_tarihi DESC"
        )
        return [self._to_user(r) for r in rows]

    def get_favorite_genres(self, kullanici_id: int) -> List[str]:
        rows = db.fetchall(
            "SELECT t.tur_adi FROM KullaniciTur kt "
            "JOIN Tur t ON kt.tur_id = t.tur_id "
            "WHERE kt.kullanici_id = ?", (kullanici_id,)
        )
        return [r[0] for r in rows]

    def set_favorite_genres(self, kullanici_id: int, tur_idler: List[int]):
        db.execute(
            "DELETE FROM KullaniciTur WHERE kullanici_id = ?",
            (kullanici_id,)
        )
        for tur_id in tur_idler:
            db.execute(
                "INSERT INTO KullaniciTur (kullanici_id, tur_id) VALUES (?, ?)",
                (kullanici_id, tur_id)
            )

    def get_stats(self, kullanici_id: int) -> dict:
        row = db.fetchone(
            "SELECT "
            "  COUNT(DISTINCT kp.program_id) AS izlenen_icerik, "
            "  COALESCE(SUM(il.izleme_suresi), 0) AS toplam_dakika, "
            "  COALESCE(AVG(CAST(kp.puan AS FLOAT)), 0) AS ort_puan "
            "FROM KullaniciProgram kp "
            "LEFT JOIN IzlemeLog il ON kp.kullanici_id = il.kullanici_id "
            "  AND kp.program_id = il.program_id "
            "WHERE kp.kullanici_id = ?",
            (kullanici_id,)
        )
        if row:
            return {
                "izlenen_icerik": row[0] or 0,
                "toplam_dakika": row[1] or 0,
                "ort_puan": round(float(row[2] or 0), 1),
            }
        return {"izlenen_icerik": 0, "toplam_dakika": 0, "ort_puan": 0.0}

    def _to_user(self, row) -> User:
        return User(
            kullanici_id=row[0],
            ad=row[1],
            soyad=row[2],
            email=row[3],
            sifre_hash=row[4],
            dogum_tarihi=row[5],
            cinsiyet=row[6],
            ulke=row[7],
            rol_id=row[8],
            aktif=bool(row[9]),
            kayit_tarihi=row[10],
        )
