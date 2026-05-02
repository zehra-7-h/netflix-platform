from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFrame, QDateEdit,
                             QComboBox, QGroupBox, QMessageBox, QGridLayout,
                             QScrollArea)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from utils.session import session


class ProfilePage(QWidget):

    def __init__(self):
        super().__init__()
        self._repo = UserRepository()
        self._auth = AuthService()
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(scroll)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(20)

        lbl = QLabel("Profilim")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(lbl)

        # İstatistik kartları
        stats_frame = QFrame()
        stats_frame.setObjectName("stat_card")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(40)
        stats_layout.setContentsMargins(24, 16, 24, 16)

        self.lbl_icerik   = self._stat(stats_layout, "Izlenen Icerik", "0")
        self.lbl_sure     = self._stat(stats_layout, "Toplam Sure", "0 dk")
        self.lbl_ort_puan = self._stat(stats_layout, "Ort. Puan", "–")
        stats_layout.addStretch()
        layout.addWidget(stats_frame)

        # Bilgi formu
        grp_bilgi = QGroupBox("Profil Bilgileri")
        form = QGridLayout(grp_bilgi)
        form.setSpacing(12)
        form.setContentsMargins(20, 20, 20, 20)
        form.setColumnMinimumWidth(0, 130)
        form.setColumnStretch(1, 1)

        def add_row(label, widget, row):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #AAAAAA; font-size: 12px;")
            form.addWidget(lbl, row, 0)
            form.addWidget(widget, row, 1)

        self.inp_ad    = QLineEdit(); self.inp_ad.setFixedHeight(38)
        self.inp_soyad = QLineEdit(); self.inp_soyad.setFixedHeight(38)
        self.inp_email = QLineEdit(); self.inp_email.setReadOnly(True); self.inp_email.setFixedHeight(38)
        self.inp_ulke  = QLineEdit(); self.inp_ulke.setFixedHeight(38)

        self.inp_dogum = QDateEdit()
        self.inp_dogum.setCalendarPopup(True)
        self.inp_dogum.setDisplayFormat("dd.MM.yyyy")
        self.inp_dogum.setFixedHeight(38)

        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.addItems(["Erkek", "Kadin", "Diger"])
        self.cmb_cinsiyet.setFixedHeight(38)

        add_row("Ad:", self.inp_ad, 0)
        add_row("Soyad:", self.inp_soyad, 1)
        add_row("E-mail:", self.inp_email, 2)
        add_row("Dogum Tarihi:", self.inp_dogum, 3)
        add_row("Cinsiyet:", self.cmb_cinsiyet, 4)
        add_row("Ulke:", self.inp_ulke, 5)

        self.lbl_fav_turler = QLabel("")
        self.lbl_fav_turler.setStyleSheet("color: #AAAAAA;")
        self.lbl_fav_turler.setWordWrap(True)
        add_row("Favori Turler:", self.lbl_fav_turler, 6)

        btn_save = QPushButton("Bilgileri Guncelle")
        btn_save.setFixedHeight(42)
        btn_save.setFixedWidth(200)
        btn_save.clicked.connect(self._save_profile)
        form.addWidget(btn_save, 7, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(grp_bilgi)

        # Şifre değiştirme
        grp_sifre = QGroupBox("Sifre Degistir")
        sifre_layout = QGridLayout(grp_sifre)
        sifre_layout.setSpacing(10)
        sifre_layout.setContentsMargins(20, 20, 20, 20)
        sifre_layout.setColumnMinimumWidth(0, 130)
        sifre_layout.setColumnStretch(1, 1)

        def sifre_row(label, row):
            lbl = QLabel(label)
            lbl.setStyleSheet("color: #AAAAAA; font-size: 12px;")
            inp = QLineEdit()
            inp.setEchoMode(QLineEdit.EchoMode.Password)
            inp.setFixedHeight(38)
            sifre_layout.addWidget(lbl, row, 0)
            sifre_layout.addWidget(inp, row, 1)
            return inp

        self.inp_eski  = sifre_row("Mevcut Sifre:", 0)
        self.inp_yeni  = sifre_row("Yeni Sifre:", 1)
        self.inp_yeni2 = sifre_row("Yeni Sifre Tekrar:", 2)

        btn_sifre = QPushButton("Sifre Guncelle")
        btn_sifre.setFixedHeight(42)
        btn_sifre.setFixedWidth(180)
        btn_sifre.clicked.connect(self._change_password)
        sifre_layout.addWidget(btn_sifre, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        self.lbl_sifre_msg = QLabel("")
        self.lbl_sifre_msg.setObjectName("lbl_success")
        sifre_layout.addWidget(self.lbl_sifre_msg, 4, 1)
        layout.addWidget(grp_sifre)
        layout.addStretch()

        scroll.setWidget(container)

    def _stat(self, parent, label, value):
        v = QVBoxLayout()
        lbl_val = QLabel(value)
        lbl_val.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl_val.setStyleSheet("color: #E50914;")
        lbl_key = QLabel(label)
        lbl_key.setStyleSheet("color: #AAAAAA; font-size: 11px;")
        v.addWidget(lbl_val)
        v.addWidget(lbl_key)
        parent.addLayout(v)
        return lbl_val

    def refresh(self):
        user = self._repo.find_by_id(session.user_id)
        if not user:
            return

        self.inp_ad.setText(user.ad)
        self.inp_soyad.setText(user.soyad)
        self.inp_email.setText(user.email)
        self.inp_ulke.setText(user.ulke or "")

        if user.dogum_tarihi:
            d = user.dogum_tarihi
            self.inp_dogum.setDate(QDate(d.year, d.month, d.day))

        idx = self.cmb_cinsiyet.findText(user.cinsiyet or "Diger")
        if idx >= 0:
            self.cmb_cinsiyet.setCurrentIndex(idx)

        turler = self._repo.get_favorite_genres(session.user_id)
        self.lbl_fav_turler.setText(", ".join(turler) if turler else "–")

        stats = self._repo.get_stats(session.user_id)
        self.lbl_icerik.setText(str(stats["izlenen_icerik"]))
        self.lbl_sure.setText(f"{stats['toplam_dakika']} dk")
        self.lbl_ort_puan.setText(
            f"{stats['ort_puan']:.1f}" if stats['ort_puan'] else "–"
        )

    def _save_profile(self):
        from datetime import date as dt
        qd = self.inp_dogum.date()
        dogum = dt(qd.year(), qd.month(), qd.day())
        self._repo.update_profile(
            session.user_id,
            self.inp_ad.text().strip(),
            self.inp_soyad.text().strip(),
            dogum,
            self.cmb_cinsiyet.currentText(),
            self.inp_ulke.text().strip()
        )
        QMessageBox.information(self, "Basarili", "Profil bilgileriniz guncellendi.")

    def _change_password(self):
        self.lbl_sifre_msg.setText("")
        ok, msg = self._auth.change_password(
            session.user_id,
            self.inp_eski.text(),
            self.inp_yeni.text(),
            self.inp_yeni2.text()
        )
        if ok:
            self.lbl_sifre_msg.setObjectName("lbl_success")
            self.lbl_sifre_msg.setText("Sifre basariyla guncellendi.")
            self.inp_eski.clear()
            self.inp_yeni.clear()
            self.inp_yeni2.clear()
        else:
            self.lbl_sifre_msg.setObjectName("lbl_error")
            self.lbl_sifre_msg.setText(msg)
