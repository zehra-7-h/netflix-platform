from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from services.auth_service import AuthService


class LoginPage(QWidget):
    login_success = pyqtSignal(object)   # User nesnesi gönderir
    go_register   = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._auth = AuthService()
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.setContentsMargins(0, 0, 0, 0)

        # Orta kart
        card = QFrame()
        card.setFixedWidth(420)
        card.setObjectName("content_card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # Logo / başlık
        lbl_logo = QLabel("N")
        lbl_logo.setFont(QFont("Arial Black", 48, QFont.Weight.Bold))
        lbl_logo.setStyleSheet("color: #E50914;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_logo)

        lbl_title = QLabel("Giris Yap")
        lbl_title.setObjectName("lbl_title")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        card_layout.addWidget(lbl_title)

        card_layout.addSpacing(8)

        # E-mail
        lbl_email = QLabel("E-mail")
        lbl_email.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        card_layout.addWidget(lbl_email)

        self.inp_email = QLineEdit()
        self.inp_email.setPlaceholderText("ornek@email.com")
        self.inp_email.setFixedHeight(44)
        card_layout.addWidget(self.inp_email)

        # Şifre
        lbl_sifre = QLabel("Sifre")
        lbl_sifre.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        card_layout.addWidget(lbl_sifre)

        sifre_row = QHBoxLayout()
        sifre_row.setSpacing(6)

        self.inp_sifre = QLineEdit()
        self.inp_sifre.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_sifre.setPlaceholderText("En az 6 karakter")
        self.inp_sifre.setFixedHeight(44)
        self.inp_sifre.returnPressed.connect(self._on_login)
        sifre_row.addWidget(self.inp_sifre)

        btn_eye_l = QPushButton("Goster")
        btn_eye_l.setObjectName("btn_secondary")
        btn_eye_l.setFixedSize(85, 44)
        btn_eye_l.setCheckable(True)
        btn_eye_l.toggled.connect(
            lambda on: (
                self.inp_sifre.setEchoMode(
                    QLineEdit.EchoMode.Normal if on
                    else QLineEdit.EchoMode.Password
                ),
                btn_eye_l.setText("Gizle" if on else "Goster"),
            )
        )
        sifre_row.addWidget(btn_eye_l)
        card_layout.addLayout(sifre_row)

        # Hata mesajı
        self.lbl_error = QLabel("")
        self.lbl_error.setObjectName("lbl_error")
        self.lbl_error.setWordWrap(True)
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.lbl_error)

        # Giriş butonu
        self.btn_login = QPushButton("Giris Yap")
        self.btn_login.setFixedHeight(44)
        self.btn_login.clicked.connect(self._on_login)
        card_layout.addWidget(self.btn_login)

        # Kayıt ol
        alt_layout = QHBoxLayout()
        lbl_hint = QLabel("Hesabiniz yok mu?")
        lbl_hint.setStyleSheet("color: #AAAAAA;")
        btn_register = QPushButton("Kayit Ol")
        btn_register.setObjectName("btn_secondary")
        btn_register.setFixedHeight(36)
        btn_register.clicked.connect(self.go_register.emit)
        alt_layout.addWidget(lbl_hint)
        alt_layout.addWidget(btn_register)
        card_layout.addLayout(alt_layout)

        root.addWidget(card)

    def _on_login(self):
        self.lbl_error.setText("")
        email = self.inp_email.text().strip()
        sifre = self.inp_sifre.text()

        self.btn_login.setEnabled(False)
        self.btn_login.setText("Kontrol ediliyor...")

        ok, msg, user = self._auth.login(email, sifre)

        self.btn_login.setEnabled(True)
        self.btn_login.setText("Giris Yap")

        if ok:
            self.inp_email.clear()
            self.inp_sifre.clear()
            self.login_success.emit(user)
        else:
            self.lbl_error.setText(msg)

    def reset(self):
        self.inp_email.clear()
        self.inp_sifre.clear()
        self.lbl_error.setText("")
