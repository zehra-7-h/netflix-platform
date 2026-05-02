import re
from datetime import date


def validate_email(email: str) -> tuple[bool, str]:
    if not email or not email.strip():
        return False, "E-mail bos birakilamaz."
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(pattern, email.strip()):
        return False, "Gecersiz e-mail formati."
    return True, ""


def validate_password(sifre: str) -> tuple[bool, str]:
    if not sifre:
        return False, "Sifre bos birakilamaz."
    if len(sifre) < 6:
        return False, "Sifre en az 6 karakter olmalidir."
    return True, ""


def validate_passwords_match(sifre: str, sifre_tekrar: str) -> tuple[bool, str]:
    if sifre != sifre_tekrar:
        return False, "Sifreler eslesmiyor."
    return True, ""


def validate_birth_date(dogum_tarihi: date) -> tuple[bool, str]:
    if dogum_tarihi >= date.today():
        return False, "Dogum tarihi bugunden buyuk olamaz."
    return True, ""


def validate_not_empty(deger: str, alan_adi: str) -> tuple[bool, str]:
    if not deger or not str(deger).strip():
        return False, f"{alan_adi} bos birakilamaz."
    return True, ""


def validate_rating(puan: int) -> tuple[bool, str]:
    if not isinstance(puan, int) or puan < 1 or puan > 10:
        return False, "Puan 1 ile 10 arasinda olmalidir."
    return True, ""


def validate_year(yil: int) -> tuple[bool, str]:
    if not yil or not str(yil).isdigit():
        return False, "Gecerli bir yayin yili giriniz."
    yil = int(yil)
    if yil < 1900 or yil > date.today().year + 1:
        return False, f"Yayin yili 1900 ile {date.today().year + 1} arasinda olmalidir."
    return True, ""


def validate_genre_count(tur_idler: list) -> tuple[bool, str]:
    if len(tur_idler) != 3:
        return False, "Tam olarak 3 farkli tur secmelisiniz."
    if len(set(tur_idler)) != 3:
        return False, "3 farkli tur secmelisiniz (ayni tur tekrar edilemez)."
    return True, ""
