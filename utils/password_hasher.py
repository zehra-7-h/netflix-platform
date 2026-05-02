try:
    import bcrypt
except ModuleNotFoundError as exc:
    bcrypt = None
    _BCRYPT_IMPORT_ERROR = exc
else:
    _BCRYPT_IMPORT_ERROR = None


def hash_password(sifre: str) -> str:
    if bcrypt is None:
        raise RuntimeError(
            "bcrypt kurulu degil. Sifreleme icin `pip install bcrypt` calistirin."
        ) from _BCRYPT_IMPORT_ERROR
    return bcrypt.hashpw(sifre.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(sifre: str, sifre_hash: str) -> bool:
    if bcrypt is None:
        raise RuntimeError(
            "bcrypt kurulu degil. Sifre dogrulama icin `pip install bcrypt` calistirin."
        ) from _BCRYPT_IMPORT_ERROR
    return bcrypt.checkpw(sifre.encode("utf-8"), sifre_hash.encode("utf-8"))
