from database.connection import db
from models.program import Genre
from typing import List, Optional


class GenreRepository:

    def get_all(self) -> List[Genre]:
        rows = db.fetchall("SELECT tur_id, tur_adi FROM Tur ORDER BY tur_adi")
        return [Genre(r[0], r[1]) for r in rows]

    def find_by_id(self, tur_id: int) -> Optional[Genre]:
        row = db.fetchone(
            "SELECT tur_id, tur_adi FROM Tur WHERE tur_id = ?", (tur_id,)
        )
        return Genre(row[0], row[1]) if row else None

    def create(self, tur_adi: str) -> int:
        existing = db.fetchone(
            "SELECT tur_id FROM Tur WHERE tur_adi = ?", (tur_adi,)
        )
        if existing:
            raise ValueError(f"'{tur_adi}' turu zaten mevcut.")
        return db.insert_and_get_id(
            "INSERT INTO Tur (tur_adi) OUTPUT INSERTED.tur_id VALUES (?)",
            (tur_adi,)
        )

    def update(self, tur_id: int, tur_adi: str):
        db.execute(
            "UPDATE Tur SET tur_adi = ? WHERE tur_id = ?", (tur_adi, tur_id)
        )

    def delete(self, tur_id: int):
        # Tüm PDF isteği: türe bağlı içerik varsa silinemez
        row = db.fetchone(
            "SELECT COUNT(*) FROM ProgramTur WHERE tur_id = ?", (tur_id,)
        )
        if row and row[0] > 0:
            raise ValueError(
                "Bu ture bagli icerikler var. Once icerikleri guncelleyin."
            )
        db.execute("DELETE FROM Tur WHERE tur_id = ?", (tur_id,))
