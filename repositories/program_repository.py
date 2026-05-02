from database.connection import db
from models.program import Program, Genre, WatchStatus, Favorite, WatchLog, Episode
from typing import Optional, List


class ProgramRepository:

    def get_all(self, tipi: str = None) -> List[Program]:
        sql = ("SELECT program_id, ad, aciklama, program_tipi, yayin_yili, "
               "bolum_sayisi, bolum_suresi, ortalama_puan, toplam_izlenme "
               "FROM Program")
        params = ()
        if tipi:
            sql += " WHERE program_tipi = ?"
            params = (tipi,)
        sql += " ORDER BY ad"
        rows = db.fetchall(sql, params)
        programs = [self._to_program(r) for r in rows]
        self._attach_genres_bulk(programs)
        return programs

    def find_by_id(self, program_id: int) -> Optional[Program]:
        row = db.fetchone(
            "SELECT program_id, ad, aciklama, program_tipi, yayin_yili, "
            "bolum_sayisi, bolum_suresi, ortalama_puan, toplam_izlenme "
            "FROM Program WHERE program_id = ?", (program_id,)
        )
        if not row:
            return None
        p = self._to_program(row)
        p.turler = self._get_genres(program_id)
        return p

    def search(self, ad: str = None, tur_id: int = None, tipi: str = None,
               yayin_yili: int = None, min_puan: float = None) -> List[Program]:
        sql = ("SELECT DISTINCT p.program_id, p.ad, p.aciklama, p.program_tipi, "
               "p.yayin_yili, p.bolum_sayisi, p.bolum_suresi, "
               "p.ortalama_puan, p.toplam_izlenme "
               "FROM Program p")
        params = []
        joins = []
        wheres = []

        if tur_id:
            joins.append("JOIN ProgramTur pt ON p.program_id = pt.program_id")
            wheres.append("pt.tur_id = ?")
            params.append(tur_id)

        if ad:
            wheres.append("p.ad LIKE ?")
            params.append(f"%{ad}%")

        if tipi:
            wheres.append("p.program_tipi = ?")
            params.append(tipi)

        if yayin_yili:
            wheres.append("p.yayin_yili = ?")
            params.append(yayin_yili)

        if min_puan is not None:
            wheres.append("p.ortalama_puan >= ?")
            params.append(min_puan)

        if joins:
            sql += " " + " ".join(joins)
        if wheres:
            sql += " WHERE " + " AND ".join(wheres)
        sql += " ORDER BY p.ortalama_puan DESC"

        rows = db.fetchall(sql, tuple(params))
        programs = [self._to_program(r) for r in rows]
        self._attach_genres_bulk(programs)
        return programs

    def get_top_rated(self, limit: int = 10) -> List[Program]:
        rows = db.fetchall(
            "SELECT TOP (?) program_id, ad, aciklama, program_tipi, yayin_yili, "
            "bolum_sayisi, bolum_suresi, ortalama_puan, toplam_izlenme "
            "FROM Program WHERE ortalama_puan > 0 "
            "ORDER BY ortalama_puan DESC", (limit,)
        )
        programs = [self._to_program(r) for r in rows]
        self._attach_genres_bulk(programs)
        return programs

    def get_most_watched(self, limit: int = 10) -> List[Program]:
        rows = db.fetchall(
            "SELECT TOP (?) program_id, ad, aciklama, program_tipi, yayin_yili, "
            "bolum_sayisi, bolum_suresi, ortalama_puan, toplam_izlenme "
            "FROM Program ORDER BY toplam_izlenme DESC", (limit,)
        )
        programs = [self._to_program(r) for r in rows]
        self._attach_genres_bulk(programs)
        return programs

    def create(self, ad, aciklama, program_tipi, yayin_yili,
               bolum_sayisi, bolum_suresi) -> int:
        return db.insert_and_get_id(
            "INSERT INTO Program (ad, aciklama, program_tipi, yayin_yili, "
            "bolum_sayisi, bolum_suresi) "
            "OUTPUT INSERTED.program_id VALUES (?, ?, ?, ?, ?, ?)",
            (ad, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_suresi)
        )

    def update(self, program_id, ad, aciklama, program_tipi,
               yayin_yili, bolum_sayisi, bolum_suresi):
        db.execute(
            "UPDATE Program SET ad=?, aciklama=?, program_tipi=?, "
            "yayin_yili=?, bolum_sayisi=?, bolum_suresi=? "
            "WHERE program_id=?",
            (ad, aciklama, program_tipi, yayin_yili,
             bolum_sayisi, bolum_suresi, program_id)
        )

    def delete(self, program_id: int):
        db.execute("DELETE FROM Program WHERE program_id = ?", (program_id,))

    def set_genres(self, program_id: int, tur_idler: List[int]):
        db.execute("DELETE FROM ProgramTur WHERE program_id = ?", (program_id,))
        for tur_id in tur_idler:
            db.execute(
                "INSERT INTO ProgramTur (program_id, tur_id) VALUES (?, ?)",
                (program_id, tur_id)
            )

    # ── İzleme işlemleri ──────────────────────────────────────

    def get_watch_status(self, kullanici_id: int, program_id: int) -> Optional[WatchStatus]:
        row = db.fetchone(
            "SELECT kullanici_id, program_id, son_bolum, son_dakika, "
            "tamamlandi, puan, son_izleme "
            "FROM KullaniciProgram WHERE kullanici_id=? AND program_id=?",
            (kullanici_id, program_id)
        )
        if not row:
            return None
        return WatchStatus(
            kullanici_id=row[0], program_id=row[1],
            son_bolum=row[2], son_dakika=row[3],
            tamamlandi=bool(row[4]), puan=row[5], son_izleme=row[6]
        )

    def upsert_watch_status(self, kullanici_id: int, program_id: int,
                            son_bolum: int, son_dakika: int, tamamlandi: bool):
        existing = self.get_watch_status(kullanici_id, program_id)
        if existing:
            db.execute(
                "UPDATE KullaniciProgram SET son_bolum=?, son_dakika=?, "
                "tamamlandi=?, son_izleme=GETDATE() "
                "WHERE kullanici_id=? AND program_id=?",
                (son_bolum, son_dakika, 1 if tamamlandi else 0,
                 kullanici_id, program_id)
            )
        else:
            db.execute(
                "INSERT INTO KullaniciProgram "
                "(kullanici_id, program_id, son_bolum, son_dakika, tamamlandi) "
                "VALUES (?, ?, ?, ?, ?)",
                (kullanici_id, program_id, son_bolum, son_dakika,
                 1 if tamamlandi else 0)
            )

    def set_rating(self, kullanici_id: int, program_id: int, puan: int):
        db.execute(
            "UPDATE KullaniciProgram SET puan=? "
            "WHERE kullanici_id=? AND program_id=?",
            (puan, kullanici_id, program_id)
        )

    def add_watch_log(self, kullanici_id: int, program_id: int,
                      izlenen_bolum: int, izleme_suresi: int, tamamlandi: bool):
        db.execute(
            "INSERT INTO IzlemeLog "
            "(kullanici_id, program_id, izlenen_bolum, izleme_suresi, tamamlandi) "
            "VALUES (?, ?, ?, ?, ?)",
            (kullanici_id, program_id, izlenen_bolum, izleme_suresi,
             1 if tamamlandi else 0)
        )

    def get_watch_history(self, kullanici_id: int) -> List[WatchLog]:
        rows = db.fetchall(
            "SELECT il.log_id, il.kullanici_id, il.program_id, "
            "il.izleme_tarihi, il.izlenen_bolum, il.izleme_suresi, "
            "il.tamamlandi, p.ad, p.program_tipi "
            "FROM IzlemeLog il "
            "JOIN Program p ON il.program_id = p.program_id "
            "WHERE il.kullanici_id = ? "
            "ORDER BY il.izleme_tarihi DESC",
            (kullanici_id,)
        )
        return [
            WatchLog(log_id=r[0], kullanici_id=r[1], program_id=r[2],
                     izleme_tarihi=r[3], izlenen_bolum=r[4],
                     izleme_suresi=r[5], tamamlandi=bool(r[6]),
                     program_adi=r[7], program_tipi=r[8])
            for r in rows
        ]

    # ── Favori işlemleri ──────────────────────────────────────

    def add_favorite(self, kullanici_id: int, program_id: int):
        existing = db.fetchone(
            "SELECT favori_id FROM Favori WHERE kullanici_id=? AND program_id=?",
            (kullanici_id, program_id)
        )
        if not existing:
            db.execute(
                "INSERT INTO Favori (kullanici_id, program_id) VALUES (?, ?)",
                (kullanici_id, program_id)
            )

    def remove_favorite(self, kullanici_id: int, program_id: int):
        db.execute(
            "DELETE FROM Favori WHERE kullanici_id=? AND program_id=?",
            (kullanici_id, program_id)
        )

    def is_favorite(self, kullanici_id: int, program_id: int) -> bool:
        row = db.fetchone(
            "SELECT favori_id FROM Favori WHERE kullanici_id=? AND program_id=?",
            (kullanici_id, program_id)
        )
        return row is not None

    def get_favorites(self, kullanici_id: int, tur_id: int = None) -> List[Favorite]:
        sql = ("SELECT f.favori_id, f.kullanici_id, f.program_id, "
               "f.eklenme_tarihi, p.ad, p.program_tipi, "
               "STRING_AGG(t.tur_adi, ', ') AS turler "
               "FROM Favori f "
               "JOIN Program p ON f.program_id = p.program_id "
               "LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id "
               "LEFT JOIN Tur t ON pt.tur_id = t.tur_id ")
        params = [kullanici_id]
        where = "WHERE f.kullanici_id = ?"
        if tur_id:
            where += (" AND f.program_id IN "
                      "(SELECT program_id FROM ProgramTur WHERE tur_id = ?)")
            params.append(tur_id)
        sql += where + " GROUP BY f.favori_id, f.kullanici_id, f.program_id, "
        sql += "f.eklenme_tarihi, p.ad, p.program_tipi ORDER BY f.eklenme_tarihi DESC"
        rows = db.fetchall(sql, tuple(params))
        return [
            Favorite(favori_id=r[0], kullanici_id=r[1], program_id=r[2],
                     eklenme_tarihi=r[3], program_adi=r[4],
                     program_tipi=r[5], turler=r[6])
            for r in rows
        ]

    # ── Bölüm işlemleri ──────────────────────────────────────

    def get_episodes(self, program_id: int) -> List[Episode]:
        rows = db.fetchall(
            "SELECT bolum_id, program_id, bolum_no, bolum_adi, sure "
            "FROM Bolum WHERE program_id = ? ORDER BY bolum_no",
            (program_id,)
        )
        return [Episode(r[0], r[1], r[2], r[3], r[4]) for r in rows]

    # ── Yardımcı metotlar ─────────────────────────────────────

    def _get_genres(self, program_id: int) -> List[Genre]:
        rows = db.fetchall(
            "SELECT t.tur_id, t.tur_adi FROM Tur t "
            "JOIN ProgramTur pt ON t.tur_id = pt.tur_id "
            "WHERE pt.program_id = ?", (program_id,)
        )
        return [Genre(r[0], r[1]) for r in rows]

    def _attach_genres_bulk(self, programs: List[Program]):
        if not programs:
            return
        ids = tuple(p.program_id for p in programs)
        placeholders = ",".join("?" * len(ids))
        rows = db.fetchall(
            f"SELECT pt.program_id, t.tur_id, t.tur_adi "
            f"FROM ProgramTur pt JOIN Tur t ON pt.tur_id = t.tur_id "
            f"WHERE pt.program_id IN ({placeholders})", ids
        )
        genre_map: dict = {}
        for r in rows:
            genre_map.setdefault(r[0], []).append(Genre(r[1], r[2]))
        for p in programs:
            p.turler = genre_map.get(p.program_id, [])

    def _to_program(self, row) -> Program:
        return Program(
            program_id=row[0], ad=row[1], aciklama=row[2],
            program_tipi=row[3], yayin_yili=row[4],
            bolum_sayisi=row[5] or 1, bolum_suresi=row[6],
            ortalama_puan=float(row[7] or 0),
            toplam_izlenme=row[8] or 0
        )
