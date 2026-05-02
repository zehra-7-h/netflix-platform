from typing import Optional
from models.user import User


class Session:
    """
    Aktif oturumu tutan Singleton.
    Hangi kullanici giris yapti, oturum id'si nedir gibi
    bilgileri tum ekranlar buradan okur.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._user = None
            cls._instance._oturum_id = None
        return cls._instance

    def login(self, user: User, oturum_id: int):
        self._user = user
        self._oturum_id = oturum_id

    def logout(self):
        self._user = None
        self._oturum_id = None

    @property
    def current_user(self) -> Optional[User]:
        return self._user

    @property
    def oturum_id(self) -> Optional[int]:
        return self._oturum_id

    @property
    def is_logged_in(self) -> bool:
        return self._user is not None

    @property
    def is_admin(self) -> bool:
        return self._user is not None and self._user.is_admin

    @property
    def user_id(self) -> Optional[int]:
        return self._user.kullanici_id if self._user else None


# Global erişim için tek örnek
session = Session()
