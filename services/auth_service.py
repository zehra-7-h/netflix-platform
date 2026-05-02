from repositories.user_repository import UserRepository
from utils.validators import (validate_email, validate_password,
                               validate_passwords_match, validate_birth_date,
                               validate_not_empty, validate_genre_count)
from utils.password_hasher import hash_password, verify_password
from utils.session import session
from database.connection import db
from models.user import User
from datetime import date
from typing import Optional


class AuthService:

    def __init__(self):
        self._repo = UserRepository()

    def login(self, email: str, sifre: str) -> tuple[bool, str, Optional[User]]:
        """
        Giris yapar.
        Returns: (basarili_mi, hata_mesaji, kullanici)
        """
        ok, msg = validate_email(email)
        if not ok:
            return False, msg, None

        if not sifre or not sifre.strip():
            return False, "Sifre bos birakilamaz.", None

        user = self._repo.find_by_email(email.strip())
        if not user:
            return False, "Bu e-mail ile kayitli kullanici bulunamadi.", None

        if not user.aktif:
            return False, "Hesabiniz pasif durumda. Lutfen yonetici ile iletisime gecin.", None

        if not verify_password(sifre, user.sifre_hash):
            return False, "Sifre yanlis. Lutfen tekrar deneyin.", None

        # Oturum logu
        oturum_id = db.insert_and_get_id(
            "INSERT INTO OturumLog (kullanici_id) "
            "OUTPUT INSERTED.oturum_id VALUES (?)",
            (user.kullanici_id,)
        )
        session.login(user, oturum_id)
        return True, "", user

    def register(self, ad: str, soyad: str, email: str, sifre: str,
                 sifre_tekrar: str, dogum_tarihi: date, cinsiyet: str,
                 ulke: str, tur_idler: list) -> tuple[bool, str]:
        """
        Yeni kullanici kaydeder.
        Returns: (basarili_mi, hata_mesaji)
        """
        # Zorunlu alan kontrolleri
        for deger, isim in [(ad, "Ad"), (soyad, "Soyad"), (ulke, "Ulke")]:
            ok, msg = validate_not_empty(deger, isim)
            if not ok:
                return False, msg

        ok, msg = validate_email(email)
        if not ok:
            return False, msg

        ok, msg = validate_password(sifre)
        if not ok:
            return False, msg

        ok, msg = validate_passwords_match(sifre, sifre_tekrar)
        if not ok:
            return False, msg

        ok, msg = validate_birth_date(dogum_tarihi)
        if not ok:
            return False, msg

        ok, msg = validate_genre_count(tur_idler)
        if not ok:
            return False, msg

        # E-mail tekrar kontrolu
        if self._repo.find_by_email(email.strip()):
            return False, "Bu e-mail adresi zaten kayitli."

        sifre_hash = hash_password(sifre)
        kullanici_id = self._repo.create(
            ad.strip(), soyad.strip(), email.strip().lower(),
            sifre_hash, dogum_tarihi, cinsiyet, ulke.strip()
        )

        if not kullanici_id:
            return False, "Kayit sirasinda bir hata olustu."

        self._repo.set_favorite_genres(kullanici_id, tur_idler)
        return True, ""

    def logout(self):
        if session.oturum_id:
            db.execute(
                "UPDATE OturumLog SET cikis_tarihi = GETDATE() "
                "WHERE oturum_id = ?", (session.oturum_id,)
            )
        session.logout()

    def change_password(self, kullanici_id: int, eski_sifre: str,
                        yeni_sifre: str, yeni_tekrar: str) -> tuple[bool, str]:
        user = self._repo.find_by_id(kullanici_id)
        if not user:
            return False, "Kullanici bulunamadi."

        if not verify_password(eski_sifre, user.sifre_hash):
            return False, "Mevcut sifre yanlis."

        ok, msg = validate_password(yeni_sifre)
        if not ok:
            return False, msg

        ok, msg = validate_passwords_match(yeni_sifre, yeni_tekrar)
        if not ok:
            return False, msg

        self._repo.update_password(kullanici_id, hash_password(yeni_sifre))
        return True, ""
