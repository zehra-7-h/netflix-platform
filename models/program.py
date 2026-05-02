from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Genre:
    tur_id: int
    tur_adi: str


@dataclass
class Episode:
    bolum_id: int
    program_id: int
    bolum_no: int
    bolum_adi: Optional[str] = None
    sure: Optional[int] = None


@dataclass
class Program:
    program_id: int
    ad: str
    program_tipi: str          # 'Film', 'Dizi', 'Tv Show'
    bolum_sayisi: int
    ortalama_puan: float
    toplam_izlenme: int
    aciklama: Optional[str] = None
    yayin_yili: Optional[int] = None
    bolum_suresi: Optional[int] = None
    eklenme_tarihi: Optional[datetime] = None
    turler: List[Genre] = field(default_factory=list)

    @property
    def is_series(self) -> bool:
        return self.program_tipi in ("Dizi", "Tv Show")

    @property
    def tur_listesi(self) -> str:
        return ", ".join(t.tur_adi for t in self.turler) if self.turler else "-"

    @property
    def sure_goster(self) -> str:
        if self.program_tipi == "Film":
            return f"{self.bolum_suresi} dk" if self.bolum_suresi else "-"
        return f"{self.bolum_sayisi} Bolum x {self.bolum_suresi or '?'} dk"

    @property
    def puan_goster(self) -> str:
        if self.ortalama_puan and self.ortalama_puan > 0:
            return f"{self.ortalama_puan:.1f} / 10"
        return "Puan yok"


@dataclass
class WatchStatus:
    """KullaniciProgram tablosuna karsilik gelir."""
    kullanici_id: int
    program_id: int
    son_bolum: int
    son_dakika: int
    tamamlandi: bool
    puan: Optional[int] = None
    son_izleme: Optional[datetime] = None


@dataclass
class Favorite:
    favori_id: int
    kullanici_id: int
    program_id: int
    eklenme_tarihi: Optional[datetime] = None
    program_adi: Optional[str] = None
    program_tipi: Optional[str] = None
    turler: Optional[str] = None


@dataclass
class WatchLog:
    """IzlemeLog tablosuna karsilik gelir."""
    log_id: int
    kullanici_id: int
    program_id: int
    izleme_tarihi: datetime
    izlenen_bolum: int
    izleme_suresi: int
    tamamlandi: bool
    program_adi: Optional[str] = None
    program_tipi: Optional[str] = None
