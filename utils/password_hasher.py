import bcrypt


def hash_password(sifre: str) -> str:
    return bcrypt.hashpw(sifre.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(sifre: str, sifre_hash: str) -> bool:
    return bcrypt.checkpw(sifre.encode("utf-8"), sifre_hash.encode("utf-8"))
