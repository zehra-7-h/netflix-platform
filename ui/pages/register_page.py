from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QFrame,
                             QComboBox, QDateEdit, QCheckBox, QScrollArea,
                             QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont
from services.auth_service import AuthService
from repositories.genre_repository import GenreRepository
from datetime import date

_ULKELER = [
    "Turkiye", "Afganistan", "Almanya", "Amerika Birlesik Devletleri",
    "Angola", "Arjantin", "Avustralya", "Avusturya", "Azerbaycan",
    "Bahreyn", "Banglades", "Belcika", "Bolivya", "Bosna Hersek",
    "Brezilya", "Bulgaristan", "Cek Cumhuriyeti", "Cezayir", "Cin",
    "Danimarka", "Ekvador", "Endonezya", "Ermenistan", "Etiyopya",
    "Filipinler", "Finlandiya", "Fransa", "Gana", "Guatemala",
    "Guney Afrika", "Guney Kore", "Hindistan", "Hirvatistan", "Hollanda",
    "Irak", "Iran", "Irlanda", "Ispanya", "Israil", "Isvec", "Isviçre",
    "Italya", "Japonya", "Kamboçya", "Kanada", "Kazakistan", "Kenya",
    "Kibris", "Kolombiya", "Kosova", "Kuba", "Kuveyt", "Kuzey Kore",
    "Lubnan", "Libya", "Litvanya", "Luksemburg", "Macaristan",
    "Makedonya", "Malezya", "Meksika", "Misir", "Moldova", "Mogolistan",
    "Nepal", "Nijerya", "Norvec", "Ozbekistan", "Pakistan", "Paraguay",
    "Peru", "Polonya", "Portekiz", "Romanya", "Rusya", "Saudi Arabistan",
    "Senegal", "Sirbistan", "Singapur", "Slovakya", "Slovenya",
    "Sri Lanka", "Sudan", "Suriye", "Tayland", "Tanzanya", "Tunus",
    "Turemenistan", "Uganda", "Ukrayna", "Urdun", "Venezuela",
    "Vietnam", "Yemen", "Yeni Zelanda", "Yunanistan", "Zimbabve",
]


class RegisterPage(QWidget):
    register_success = pyqtSignal()
    go_login         = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._auth  = AuthService()
        self._genre = GenreRepository()
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Scroll area — form uzun olduğu için
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        root = QVBoxLayout(container)
        root.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        root.setContentsMargins(40, 30, 40, 30)
        root.setSpacing(0)

        # Kart
        card = QFrame()
        card.setFixedWidth(520)
        card.setObjectName("content_card")
        form = QVBoxLayout(card)
        form.setSpacing(12)
        form.setContentsMargins(40, 36, 40, 36)

        # Başlık
        lbl_logo = QLabel("N")
        lbl_logo.setFont(QFont("Arial Black", 36, QFont.Weight.Bold))
        lbl_logo.setStyleSheet("color: #E50914;")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addWidget(lbl_logo)

        lbl_title = QLabel("Hesap Olustur")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addWidget(lbl_title)
        form.addSpacing(12)

        # Ad / Soyad
        row1 = QHBoxLayout()
        row1.setSpacing(12)
        self.inp_ad    = self._make_field("Ad *", "Adiniz", row1)
        self.inp_soyad = self._make_field("Soyad *", "Soyadiniz", row1)
        form.addLayout(row1)

        # E-mail
        self.inp_email = self._add_field(form, "E-mail *", "ornek@email.com")

        # Şifre
        self.inp_sifre = self._add_field(
            form, "Sifre *", "En az 6 karakter", password=True)

        # Şifre tekrar
        self.inp_sifre2 = self._add_field(
            form, "Sifre Tekrar *", "Sifrenizi tekrar girin", password=True)

        # Doğum tarihi
        form.addWidget(self._lbl("Dogum Tarihi *"))
        self.inp_dogum = QDateEdit()
        self.inp_dogum.setCalendarPopup(True)
        self.inp_dogum.setDate(QDate(2000, 1, 1))
        self.inp_dogum.setMaximumDate(QDate.currentDate())
        self.inp_dogum.setDisplayFormat("dd.MM.yyyy")
        self.inp_dogum.setFixedHeight(40)
        form.addWidget(self.inp_dogum)

        # Cinsiyet / Ülke
        row2 = QHBoxLayout()
        row2.setSpacing(12)

        v_cins = QVBoxLayout()
        v_cins.addWidget(self._lbl("Cinsiyet"))
        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.addItems(["Erkek", "Kadin", "Diger"])
        self.cmb_cinsiyet.setFixedHeight(40)
        v_cins.addWidget(self.cmb_cinsiyet)

        v_ulke = QVBoxLayout()
        v_ulke.addWidget(self._lbl("Ulke *"))
        self.cmb_ulke = QComboBox()
        self.cmb_ulke.setFixedHeight(40)
        self.cmb_ulke.setMaxVisibleItems(12)
        self.cmb_ulke.addItems(_ULKELER)
        v_ulke.addWidget(self.cmb_ulke)

        row2.addLayout(v_cins)
        row2.addLayout(v_ulke)
        form.addLayout(row2)

        # Favori türler (tam olarak 3 seçilmeli)
        grp = QGroupBox("Favori Turlerinizi Secin (tam 3 adet) *")
        grp.setStyleSheet("QGroupBox { color: #E50914; }")
        grp_layout = QVBoxLayout(grp)
        grp_layout.setSpacing(6)

        self._tur_checkboxes = []
        turler = self._genre.get_all()
        grid = QGridLayout()
        grid.setSpacing(4)
        for i, tur in enumerate(turler):
            cb = QCheckBox(tur.tur_adi)
            cb.setProperty("tur_id", tur.tur_id)
            cb.stateChanged.connect(self._on_tur_changed)
            self._tur_checkboxes.append(cb)
            grid.addWidget(cb, i // 2, i % 2)

        grp_layout.addLayout(grid)

        self.lbl_tur_count = QLabel("Secilen: 0 / 3")
        self.lbl_tur_count.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        grp_layout.addWidget(self.lbl_tur_count)
        form.addWidget(grp)

        # Hata mesajı
        self.lbl_error = QLabel("")
        self.lbl_error.setObjectName("lbl_error")
        self.lbl_error.setWordWrap(True)
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addWidget(self.lbl_error)

        # Kayıt butonu
        self.btn_register = QPushButton("Kayit Ol")
        self.btn_register.setFixedHeight(44)
        self.btn_register.clicked.connect(self._on_register)
        form.addWidget(self.btn_register)

        # Giriş yap linki
        row_login = QHBoxLayout()
        lbl_hint = QLabel("Zaten hesabiniz var mi?")
        lbl_hint.setStyleSheet("color: #AAAAAA;")
        btn_login = QPushButton("Giris Yap")
        btn_login.setObjectName("btn_secondary")
        btn_login.setFixedHeight(36)
        btn_login.clicked.connect(self.go_login.emit)
        row_login.addWidget(lbl_hint)
        row_login.addWidget(btn_login)
        form.addLayout(row_login)

        root.addWidget(card)
        scroll.setWidget(container)
        outer.addWidget(scroll)

    # ── Yardımcı widget üreticileri ────────────────────────────

    def _lbl(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        return l

    def _add_field(self, layout, label: str, placeholder: str,
                   password=False) -> QLineEdit:
        layout.addWidget(self._lbl(label))
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(40)

        if not password:
            layout.addWidget(inp)
            return inp

        # Şifre: input + "Goster/Gizle" butonu yan yana
        inp.setEchoMode(QLineEdit.EchoMode.Password)
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(inp)

        btn_eye = QPushButton("Goster")
        btn_eye.setObjectName("btn_secondary")
        btn_eye.setFixedSize(85, 40)
        btn_eye.setCheckable(True)
        btn_eye.toggled.connect(
            lambda on: (
                inp.setEchoMode(
                    QLineEdit.EchoMode.Normal if on
                    else QLineEdit.EchoMode.Password
                ),
                btn_eye.setText("Gizle" if on else "Goster"),
            )
        )
        row.addWidget(btn_eye)
        layout.addLayout(row)
        return inp

    def _make_field(self, label: str, placeholder: str,
                    row_layout) -> QLineEdit:
        v = QVBoxLayout()
        v.addWidget(self._lbl(label))
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(40)
        v.addWidget(inp)
        row_layout.addLayout(v)
        return inp

    # ── Tür checkbox mantığı ───────────────────────────────────

    def _on_tur_changed(self):
        secilen = [cb for cb in self._tur_checkboxes if cb.isChecked()]
        count = len(secilen)
        self.lbl_tur_count.setText(f"Secilen: {count} / 3")
        if count >= 3:
            for cb in self._tur_checkboxes:
                if not cb.isChecked():
                    cb.setEnabled(False)
        else:
            for cb in self._tur_checkboxes:
                cb.setEnabled(True)
        if count == 3:
            self.lbl_tur_count.setStyleSheet("color: #1DB954; font-size: 12px;")
        else:
            self.lbl_tur_count.setStyleSheet("color: #AAAAAA; font-size: 12px;")

    def _get_selected_genres(self) -> list:
        return [
            cb.property("tur_id")
            for cb in self._tur_checkboxes
            if cb.isChecked()
        ]

    # ── Kayıt işlemi ──────────────────────────────────────────

    def _on_register(self):
        self.lbl_error.setText("")

        qdate = self.inp_dogum.date()
        dogum = date(qdate.year(), qdate.month(), qdate.day())
        tur_idler = self._get_selected_genres()

        self.btn_register.setEnabled(False)
        self.btn_register.setText("Kaydediliyor...")

        ok, msg = self._auth.register(
            ad=self.inp_ad.text(),
            soyad=self.inp_soyad.text(),
            email=self.inp_email.text(),
            sifre=self.inp_sifre.text(),
            sifre_tekrar=self.inp_sifre2.text(),
            dogum_tarihi=dogum,
            cinsiyet=self.cmb_cinsiyet.currentText(),
            ulke=self.cmb_ulke.currentText(),
            tur_idler=tur_idler
        )

        self.btn_register.setEnabled(True)
        self.btn_register.setText("Kayit Ol")

        if ok:
            QMessageBox.information(
                self, "Basarili",
                "Hesabiniz olusturuldu!\nSimdi giris yapabilirsiniz."
            )
            self._reset()
            self.register_success.emit()
        else:
            self.lbl_error.setText(msg)

    def _reset(self):
        for inp in [self.inp_ad, self.inp_soyad, self.inp_email,
                    self.inp_sifre, self.inp_sifre2]:
            inp.clear()
        self.cmb_ulke.setCurrentIndex(0)
        for cb in self._tur_checkboxes:
            cb.setChecked(False)
            cb.setEnabled(True)
        self.lbl_tur_count.setText("Secilen: 0 / 3")
        self.lbl_error.setText("")
