from repositories.program_repository import ProgramRepository
from repositories.genre_repository import GenreRepository
from utils.validators import validate_rating, validate_not_empty
from models.program import Program, Genre, WatchStatus, Favorite, WatchLog
from typing import List, Optional


class ContentService:

    def __init__(self):
        self._repo = ProgramRepository()
        self._genre_repo = GenreRepository()

    # ── Listeleme / Arama ─────────────────────────────────────

    def get_all(self, tipi: str = None) -> List[Program]:
        return self._repo.get_all(tipi)

    def get_by_id(self, program_id: int) -> Optional[Program]:
        return self._repo.find_by_id(program_id)

    def search(self, ad: str = None, tur_id: int = None, tipi: str = None,
               yayin_yili: int = None, min_puan: float = None) -> List[Program]:
        return self._repo.search(ad, tur_id, tipi, yayin_yili, min_puan)

    def get_top_rated(self, limit: int = 10) -> List[Program]:
        return self._repo.get_top_rated(limit)

    def get_most_watched(self, limit: int = 10) -> List[Program]:
        return self._repo.get_most_watched(limit)

    def get_genres(self) -> List[Genre]:
        return self._genre_repo.get_all()

    # ── İzleme ────────────────────────────────────────────────

    def get_watch_status(self, kullanici_id: int,
                         program_id: int) -> Optional[WatchStatus]:
        return self._repo.get_watch_status(kullanici_id, program_id)

    def save_progress(self, kullanici_id: int, program_id: int,
                      bolum: int, dakika: int, tamamlandi: bool):
        """Izleme konumunu kaydeder ve log ekler."""
        self._repo.upsert_watch_status(
            kullanici_id, program_id, bolum, dakika, tamamlandi
        )
        self._repo.add_watch_log(
            kullanici_id, program_id, bolum, dakika, tamamlandi
        )

    def get_watch_history(self, kullanici_id: int) -> List[WatchLog]:
        return self._repo.get_watch_history(kullanici_id)

    # ── Puanlama ──────────────────────────────────────────────

    def rate(self, kullanici_id: int, program_id: int,
             puan: int) -> tuple[bool, str]:
        """
        Puan verir veya gunceller.
        Kural: yalnizca izlenen iceriklere puan verilebilir.
        """
        ok, msg = validate_rating(puan)
        if not ok:
            return False, msg

        status = self._repo.get_watch_status(kullanici_id, program_id)
        if not status:
            return False, "Yalnizca izlediginiz iceriklere puan verebilirsiniz."

        self._repo.set_rating(kullanici_id, program_id, puan)
        return True, ""

    # ── Favori ────────────────────────────────────────────────

    def toggle_favorite(self, kullanici_id: int,
                        program_id: int) -> bool:
        """Favoriye ekler ya da cikarir. Yeni durumu (True=eklendi) doner."""
        if self._repo.is_favorite(kullanici_id, program_id):
            self._repo.remove_favorite(kullanici_id, program_id)
            return False
        else:
            self._repo.add_favorite(kullanici_id, program_id)
            return True

    def is_favorite(self, kullanici_id: int, program_id: int) -> bool:
        return self._repo.is_favorite(kullanici_id, program_id)

    def get_favorites(self, kullanici_id: int,
                      tur_id: int = None) -> List[Favorite]:
        return self._repo.get_favorites(kullanici_id, tur_id)

    def get_episodes(self, program_id: int):
        return self._repo.get_episodes(program_id)
