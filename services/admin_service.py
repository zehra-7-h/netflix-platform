from repositories.program_repository import ProgramRepository
from repositories.genre_repository import GenreRepository
from repositories.user_repository import UserRepository
from repositories.report_repository import ReportRepository
from utils.validators import validate_not_empty, validate_year
from typing import List


class AdminService:

    def __init__(self):
        self._prog = ProgramRepository()
        self._genre = GenreRepository()
        self._user = UserRepository()
        self._report = ReportRepository()

    # ── İçerik Yönetimi ──────────────────────────────────────

    def add_program(self, ad, aciklama, program_tipi,
                    yayin_yili, bolum_sayisi, bolum_suresi,
                    tur_idler: List[int]) -> tuple[bool, str]:
        ok, msg = validate_not_empty(ad, "Program adi")
        if not ok:
            return False, msg

        ok, msg = validate_not_empty(program_tipi, "Program tipi")
        if not ok:
            return False, msg

        if yayin_yili:
            ok, msg = validate_year(yayin_yili)
            if not ok:
                return False, msg

        try:
            pid = self._prog.create(
                ad.strip(), aciklama, program_tipi,
                yayin_yili, bolum_sayisi or 1, bolum_suresi
            )
            if tur_idler:
                self._prog.set_genres(pid, tur_idler)
            return True, ""
        except Exception as e:
            return False, str(e)

    def update_program(self, program_id, ad, aciklama, program_tipi,
                       yayin_yili, bolum_sayisi, bolum_suresi,
                       tur_idler: List[int]) -> tuple[bool, str]:
        ok, msg = validate_not_empty(ad, "Program adi")
        if not ok:
            return False, msg
        try:
            self._prog.update(
                program_id, ad.strip(), aciklama, program_tipi,
                yayin_yili, bolum_sayisi or 1, bolum_suresi
            )
            if tur_idler:
                self._prog.set_genres(program_id, tur_idler)
            return True, ""
        except Exception as e:
            return False, str(e)

    def delete_program(self, program_id: int) -> tuple[bool, str]:
        try:
            self._prog.delete(program_id)
            return True, ""
        except Exception as e:
            return False, str(e)

    # ── Tür Yönetimi ─────────────────────────────────────────

    def add_genre(self, tur_adi: str) -> tuple[bool, str]:
        ok, msg = validate_not_empty(tur_adi, "Tur adi")
        if not ok:
            return False, msg
        try:
            self._genre.create(tur_adi.strip())
            return True, ""
        except ValueError as e:
            return False, str(e)

    def update_genre(self, tur_id: int, tur_adi: str) -> tuple[bool, str]:
        ok, msg = validate_not_empty(tur_adi, "Tur adi")
        if not ok:
            return False, msg
        try:
            self._genre.update(tur_id, tur_adi.strip())
            return True, ""
        except Exception as e:
            return False, str(e)

    def delete_genre(self, tur_id: int) -> tuple[bool, str]:
        try:
            self._genre.delete(tur_id)
            return True, ""
        except ValueError as e:
            return False, str(e)

    # ── Kullanıcı Yönetimi ────────────────────────────────────

    def get_all_users(self):
        return self._user.get_all_users()

    def set_user_active(self, kullanici_id: int, aktif: bool) -> tuple[bool, str]:
        try:
            self._user.set_active(kullanici_id, aktif)
            return True, ""
        except Exception as e:
            return False, str(e)

    def get_user_stats(self, kullanici_id: int) -> dict:
        return self._user.get_stats(kullanici_id)

    def get_user_watch_history(self, kullanici_id: int):
        return ProgramRepository().get_watch_history(kullanici_id)

    # ── Raporlar ─────────────────────────────────────────────

    def top_watched(self, limit=10):
        return self._report.top_watched(limit)

    def top_rated(self, limit=10):
        return self._report.top_rated(limit)

    def top_genres(self):
        return self._report.top_genres()

    def most_active_users(self, limit=10):
        return self._report.most_active_users(limit)

    def last_7_days(self):
        return self._report.last_7_days()

    def summary(self):
        return self._report.summary()
