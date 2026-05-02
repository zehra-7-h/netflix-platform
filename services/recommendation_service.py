from database.connection import db
from repositories.program_repository import ProgramRepository
from models.program import Program
from typing import List


class RecommendationService:

    def __init__(self):
        self._repo = ProgramRepository()

    def get_registration_recommendations(self,
                                          kullanici_id: int) -> List[dict]:
        """
        Kayit sonrasi oneri: secilen 3 turden her birinden
        en yuksek puanli 2 icerik = toplam 6 oneri.
        """
        rows = db.fetchall(
            "SELECT kt.tur_id, t.tur_adi FROM KullaniciTur kt "
            "JOIN Tur t ON kt.tur_id = t.tur_id "
            "WHERE kt.kullanici_id = ?", (kullanici_id,)
        )
        result = []
        for tur_id, tur_adi in rows:
            programs = db.fetchall(
                "SELECT TOP 2 p.program_id, p.ad, p.program_tipi, "
                "p.ortalama_puan FROM Program p "
                "JOIN ProgramTur pt ON p.program_id = pt.program_id "
                "WHERE pt.tur_id = ? AND p.ortalama_puan > 0 "
                "ORDER BY p.ortalama_puan DESC", (tur_id,)
            )
            for pid, pad, ptipi, ppuan in programs:
                result.append({
                    "program_id": pid, "ad": pad,
                    "tip": ptipi, "puan": float(ppuan or 0),
                    "tur_adi": tur_adi,
                    "neden": f"{tur_adi} turunu sevdiginiz icin onerildi"
                })
        return result

    def get_personalized(self, kullanici_id: int,
                          limit: int = 10) -> List[dict]:
        """
        Kisisel oneri:
        1. Kullanicinin izledigi turlere gore
        2. Yuksek puan verdigi iceriklerin turleri
        3. Genel populer icerikler (fallback)
        """
        izlenen_ids = {
            r[0] for r in db.fetchall(
                "SELECT program_id FROM KullaniciProgram WHERE kullanici_id = ?",
                (kullanici_id,)
            )
        }

        # İzlenen ve yüksek puan verilen türleri bul
        tur_rows = db.fetchall(
            "SELECT DISTINCT pt.tur_id FROM KullaniciProgram kp "
            "JOIN ProgramTur pt ON kp.program_id = pt.program_id "
            "WHERE kp.kullanici_id = ? "
            "UNION "
            "SELECT DISTINCT pt.tur_id FROM KullaniciProgram kp "
            "JOIN ProgramTur pt ON kp.program_id = pt.program_id "
            "WHERE kp.kullanici_id = ? AND kp.puan >= 7",
            (kullanici_id, kullanici_id)
        )
        tur_ids = [r[0] for r in tur_rows]

        result = []
        if tur_ids:
            placeholders = ",".join("?" * len(tur_ids))
            rows = db.fetchall(
                f"SELECT DISTINCT TOP ({limit * 3}) p.program_id, p.ad, "
                f"p.program_tipi, p.ortalama_puan "
                f"FROM Program p "
                f"JOIN ProgramTur pt ON p.program_id = pt.program_id "
                f"WHERE pt.tur_id IN ({placeholders}) "
                f"ORDER BY p.ortalama_puan DESC",
                tuple(tur_ids)
            )
            seen_ids: set = set()
            for pid, pad, ptipi, ppuan in rows:
                if pid not in izlenen_ids and pid not in seen_ids:
                    seen_ids.add(pid)
                    result.append({
                        "program_id": pid, "ad": pad, "tip": ptipi,
                        "puan": float(ppuan or 0), "tur_adi": "",
                        "neden": "Begendiklerinizle ayni turde"
                    })
                    if len(result) >= limit:
                        break

        # Yeterli oneri yoksa populer içeriklerle doldur
        if len(result) < limit:
            pop_rows = db.fetchall(
                f"SELECT TOP ({limit}) program_id, ad, program_tipi, "
                f"ortalama_puan FROM Program "
                f"ORDER BY toplam_izlenme DESC"
            )
            for pid, pad, ptipi, ppuan in pop_rows:
                if pid not in izlenen_ids and pid not in {r["program_id"] for r in result}:
                    result.append({
                        "program_id": pid, "ad": pad, "tip": ptipi,
                        "puan": float(ppuan or 0), "tur_adi": "",
                        "neden": "En cok izlenen iceriklerden"
                    })
                if len(result) >= limit:
                    break

        return result[:limit]
