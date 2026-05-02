from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QMessageBox, QSpinBox,
                             QGroupBox, QScrollArea)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from services.content_service import ContentService
from utils.session import session


class ContentDetailPage(QWidget):
    back_requested  = pyqtSignal()
    watch_requested = pyqtSignal(object)  # Program nesnesi

    def __init__(self):
        super().__init__()
        self._svc     = ContentService()
        self._program = None
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Geri
        btn_back = QPushButton("← Geri Don")
        btn_back.setObjectName("btn_secondary")
        btn_back.setFixedWidth(140)
        btn_back.clicked.connect(self.back_requested.emit)
        layout.addWidget(btn_back)

        # Başlık + tip
        header = QHBoxLayout()
        self.lbl_title = QLabel("")
        self.lbl_title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        self.lbl_title.setWordWrap(True)
        header.addWidget(self.lbl_title, 1)

        self.lbl_tip_badge = QLabel("")
        self.lbl_tip_badge.setFixedHeight(28)
        self.lbl_tip_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_tip_badge.setStyleSheet(
            "background:#E50914; color:#fff; border-radius:4px;"
            "padding:2px 10px; font-weight:bold; font-size:12px;"
        )
        header.addWidget(self.lbl_tip_badge)
        layout.addLayout(header)

        # Meta bilgiler satırı
        self.lbl_meta = QLabel("")
        self.lbl_meta.setObjectName("lbl_subtitle")
        self.lbl_meta.setWordWrap(True)
        layout.addWidget(self.lbl_meta)

        # Türler
        self.lbl_turler = QLabel("")
        self.lbl_turler.setStyleSheet("color: #AAAAAA; font-size: 13px;")
        self.lbl_turler.setWordWrap(True)
        layout.addWidget(self.lbl_turler)

        # Ayırıcı
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #333;")
        layout.addWidget(line)

        # Açıklama
        lbl_aciklama_title = QLabel("Aciklama")
        lbl_aciklama_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(lbl_aciklama_title)

        self.lbl_aciklama = QLabel("")
        self.lbl_aciklama.setWordWrap(True)
        self.lbl_aciklama.setStyleSheet("color: #CCCCCC; font-size: 13px; line-height: 1.5;")
        layout.addWidget(self.lbl_aciklama)

        # İstatistikler
        stats_frame = QFrame()
        stats_frame.setObjectName("stat_card")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(40)

        self.lbl_puan   = self._stat_widget(stats_layout, "Ortalama Puan", "–")
        self.lbl_izlenme= self._stat_widget(stats_layout, "Izlenme Sayisi", "0")
        self.lbl_yil    = self._stat_widget(stats_layout, "Yayin Yili", "–")
        self.lbl_sure   = self._stat_widget(stats_layout, "Sure", "–")
        self.lbl_bolum  = self._stat_widget(stats_layout, "Bolum Sayisi", "1")
        stats_layout.addStretch()
        layout.addWidget(stats_frame)

        # Kullanıcı durumu
        self.grp_user = QGroupBox("Sizin Durumunuz")
        user_layout = QHBoxLayout(self.grp_user)
        self.lbl_izlendi    = QLabel("")
        self.lbl_puan_user  = QLabel("")
        self.lbl_kaldi      = QLabel("")
        for lbl in [self.lbl_izlendi, self.lbl_puan_user, self.lbl_kaldi]:
            lbl.setStyleSheet("color: #AAAAAA; font-size: 13px;")
            user_layout.addWidget(lbl)
        user_layout.addStretch()
        layout.addWidget(self.grp_user)

        # Puan verme (sadece izlendiyse görünür)
        self.grp_rating = QGroupBox("Puan Ver")
        rating_layout = QHBoxLayout(self.grp_rating)
        self.spn_puan = QSpinBox()
        self.spn_puan.setMinimum(1)
        self.spn_puan.setMaximum(10)
        self.spn_puan.setValue(7)
        self.spn_puan.setFixedHeight(40)
        self.spn_puan.setFixedWidth(80)
        rating_layout.addWidget(self.spn_puan)
        rating_layout.addWidget(QLabel("/ 10"))
        btn_rate = QPushButton("Puan Gonder")
        btn_rate.setObjectName("btn_success")
        btn_rate.setFixedHeight(40)
        btn_rate.clicked.connect(self._do_rate)
        rating_layout.addWidget(btn_rate)
        rating_layout.addStretch()
        layout.addWidget(self.grp_rating)

        # Aksiyonlar
        act_layout = QHBoxLayout()
        act_layout.setSpacing(12)

        self.btn_izle = QPushButton("▶  Izle")
        self.btn_izle.setFixedHeight(46)
        self.btn_izle.setFixedWidth(160)
        self.btn_izle.clicked.connect(self._do_watch)
        act_layout.addWidget(self.btn_izle)

        self.btn_fav = QPushButton("♡  Favoriye Ekle")
        self.btn_fav.setObjectName("btn_secondary")
        self.btn_fav.setFixedHeight(46)
        self.btn_fav.setFixedWidth(180)
        self.btn_fav.clicked.connect(self._do_favorite)
        act_layout.addWidget(self.btn_fav)

        self.btn_devam = QPushButton("⏩  Kaldigin Yerden Devam Et")
        self.btn_devam.setFixedHeight(46)
        self.btn_devam.setVisible(False)
        self.btn_devam.clicked.connect(self._do_watch)
        act_layout.addWidget(self.btn_devam)

        act_layout.addStretch()
        layout.addLayout(act_layout)

        self.lbl_msg = QLabel("")
        self.lbl_msg.setObjectName("lbl_success")
        layout.addWidget(self.lbl_msg)
        layout.addStretch()

        scroll.setWidget(container)
        outer.addWidget(scroll)

    def _stat_widget(self, parent_layout, label: str, value: str):
        v = QVBoxLayout()
        lbl_val = QLabel(value)
        lbl_val.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl_val.setStyleSheet("color: #E50914;")
        lbl_key = QLabel(label)
        lbl_key.setStyleSheet("color: #AAAAAA; font-size: 11px;")
        v.addWidget(lbl_val)
        v.addWidget(lbl_key)
        parent_layout.addLayout(v)
        return lbl_val

    def load(self, program):
        self._program = program
        uid = session.user_id
        self.lbl_msg.setText("")

        self.lbl_title.setText(program.ad)
        self.lbl_tip_badge.setText(program.program_tipi)
        self.lbl_turler.setText("Turler: " + program.tur_listesi)
        self.lbl_aciklama.setText(program.aciklama or "Aciklama girilmemis.")
        self.lbl_puan.setText(
            f"{program.ortalama_puan:.1f}" if program.ortalama_puan > 0 else "–"
        )
        self.lbl_izlenme.setText(str(program.toplam_izlenme))
        self.lbl_yil.setText(str(program.yayin_yili) if program.yayin_yili else "–")
        self.lbl_sure.setText(program.sure_goster)
        self.lbl_bolum.setText(str(program.bolum_sayisi))

        meta_parts = []
        if program.yayin_yili:
            meta_parts.append(str(program.yayin_yili))
        if program.bolum_suresi:
            meta_parts.append(f"{program.bolum_suresi} dk")
        if program.bolum_sayisi > 1:
            meta_parts.append(f"{program.bolum_sayisi} bolum")
        self.lbl_meta.setText("  •  ".join(meta_parts))

        # Kullanıcı durumu
        status = self._svc.get_watch_status(uid, program.program_id)
        if status:
            self.lbl_izlendi.setText("✓ Izlediniz")
            self.lbl_izlendi.setStyleSheet("color: #1DB954; font-size: 13px;")
            if status.puan:
                self.lbl_puan_user.setText(f"  |  Puaniniz: {status.puan}/10")
                self.spn_puan.setValue(status.puan)
            else:
                self.lbl_puan_user.setText("  |  Puan vermediniz")
            if status.son_bolum > 1 or status.son_dakika > 0:
                self.lbl_kaldi.setText(
                    f"  |  Bolum {status.son_bolum}, {status.son_dakika}. dk"
                )
                self.btn_devam.setVisible(True)
                self.btn_devam.setText(
                    f"⏩  Bolum {status.son_bolum}, {status.son_dakika}. dakikadan devam"
                )
            else:
                self.btn_devam.setVisible(False)
            self.grp_rating.setVisible(True)
        else:
            self.lbl_izlendi.setText("Henuz izlemediniz")
            self.lbl_izlendi.setStyleSheet("color: #AAAAAA; font-size: 13px;")
            self.lbl_puan_user.setText("")
            self.lbl_kaldi.setText("")
            self.btn_devam.setVisible(False)
            self.grp_rating.setVisible(False)

        # Favori butonu
        is_fav = self._svc.is_favorite(uid, program.program_id)
        self._update_fav_btn(is_fav)

    def _update_fav_btn(self, is_fav: bool):
        if is_fav:
            self.btn_fav.setText("♥  Favorilerden Cikar")
            self.btn_fav.setStyleSheet("background-color: #E50914;")
        else:
            self.btn_fav.setText("♡  Favoriye Ekle")
            self.btn_fav.setStyleSheet("")

    def _do_watch(self):
        if self._program:
            self.watch_requested.emit(self._program)

    def _do_favorite(self):
        if not self._program:
            return
        is_now_fav = self._svc.toggle_favorite(
            session.user_id, self._program.program_id
        )
        self._update_fav_btn(is_now_fav)
        self.lbl_msg.setText(
            "Favorilere eklendi." if is_now_fav else "Favorilerden cikarildi."
        )

    def _do_rate(self):
        if not self._program:
            return
        puan = self.spn_puan.value()
        ok, msg = self._svc.rate(
            session.user_id, self._program.program_id, puan
        )
        if ok:
            self.lbl_puan_user.setText(f"  |  Puaniniz: {puan}/10")
            QMessageBox.information(self, "Basarili", f"Puaniniz {puan}/10 olarak kaydedildi.")
        else:
            QMessageBox.warning(self, "Hata", msg)
