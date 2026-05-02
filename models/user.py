from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Role:
    rol_id: int
    rol_adi: str


@dataclass
class User:
    kullanici_id: int
    ad: str
    soyad: str
    email: str
    dogum_tarihi: date
    rol_id: int
    aktif: bool
    kayit_tarihi: datetime
    cinsiyet: Optional[str] = None
    ulke: Optional[str] = None
    sifre_hash: str = ""

    @property
    def tam_ad(self) -> str:
        return f"{self.ad} {self.soyad}"

    @property
    def is_admin(self) -> bool:
        return self.rol_id == 2

    @property
    def yas(self) -> int:
        bugun = date.today()
        d = self.dogum_tarihi if isinstance(self.dogum_tarihi, date) else self.dogum_tarihi.date()
        return bugun.year - d.year - ((bugun.month, bugun.day) < (d.month, d.day))
