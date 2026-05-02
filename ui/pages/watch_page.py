from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSpinBox, QMessageBox, QFrame,
                             QSlider, QGroupBox, QComboBox, QProgressBar,
                             QSizePolicy)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from services.content_service import ContentService
from utils.session import session


class WatchPage(QWidget):
    back_requested = pyqtSignal()
    watch_saved    = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._svc = ContentService()
        self._program = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Geri butonu
        btn_back = QPushButton("← Geri Don")
        btn_back.setObjectName("btn_secondary")
        btn_back.setFixedWidth(140)
        btn_back.clicked.connect(self.back_requested.emit)
        layout.addWidget(btn_back)

        # İçerik başlığı
        self.lbl_title = QLabel("")
        self.lbl_title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        layout.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel("")
        self.lbl_subtitle.setObjectName("lbl_subtitle")
        layout.addWidget(self.lbl_subtitle)

        # İzleme ekranı simülasyonu
        screen = QFrame()
        screen.setMinimumHeight(300)
        screen.setStyleSheet("background-color: #000; border-radius: 8px;")
        screen_layout = QVBoxLayout(screen)
        screen_layout.setContentsMargins(0, 0, 0, 14)
        screen_layout.setSpacing(0)

        # Orta alan — play butonu (esnetilir)
        center_w = QWidget()
        center_w.setStyleSheet("background: transparent;")
        center_w.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        center_l = QVBoxLayout(center_w)
        center_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_l.setSpacing(12)

        lbl_brand = QLabel("NETFLIX PLATFORM")
        lbl_brand.setStyleSheet(
            "color: rgba(255,255,255,18); font-size: 11px; letter-spacing: 5px;"
        )
        lbl_brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_l.addWidget(lbl_brand)

        # Play butonu — büyük ve okunaklı
        lbl_play = QLabel("▶")
        lbl_play.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_play.setFixedSize(100, 100)
        lbl_play.setStyleSheet(
            "color: white;"
            "background: rgba(229,9,20,220);"
            "border-radius: 50px;"
            "font-size: 46px;"
            "padding-left: 6px;"
        )
        center_l.addWidget(lbl_play, alignment=Qt.AlignmentFlag.AlignCenter)
        screen_layout.addWidget(center_w, 1)

        # Alt bilgi çubuğu — doğrudan screen_layout içinde
        self.lbl_screen_info = QLabel("Oynatiliyor...")
        self.lbl_screen_info.setStyleSheet(
            "color: white; font-size: 13px; font-weight: bold;"
            "padding-left: 16px; padding-right: 16px; padding-top: 6px;"
            "background: transparent;"
        )
        screen_layout.addWidget(self.lbl_screen_info)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFixedHeight(5)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setStyleSheet(
            "QProgressBar {"
            "  background: #333; border-radius: 2px; border: none;"
            "  margin-left: 16px; margin-right: 16px;"
            "}"
            "QProgressBar::chunk { background: #E50914; border-radius: 2px; }"
        )
        screen_layout.addWidget(self._progress_bar)

        time_w = QWidget()
        time_w.setStyleSheet("background: transparent;")
        time_l = QHBoxLayout(time_w)
        time_l.setContentsMargins(16, 2, 16, 10)
        time_l.setSpacing(0)
        self._lbl_time_cur = QLabel("00:00")
        self._lbl_time_cur.setStyleSheet("color: #888; font-size: 11px;")
        time_l.addWidget(self._lbl_time_cur)
        time_l.addStretch()
        self._lbl_time_tot = QLabel("00:00")
        self._lbl_time_tot.setStyleSheet("color: #888; font-size: 11px;")
        time_l.addWidget(self._lbl_time_tot)
        screen_layout.addWidget(time_w)

        layout.addWidget(screen)

        # Bölüm ve süre
        controls = QGroupBox("Izleme Kontrolu")
        ctrl_layout = QHBoxLayout(controls)
        ctrl_layout.setSpacing(24)

        # Bölüm no
        v_bolum = QVBoxLayout()
        v_bolum.addWidget(QLabel("Bolum No:"))
        self.spn_bolum = QSpinBox()
        self.spn_bolum.setMinimum(1)
        self.spn_bolum.setMaximum(9999)
        self.spn_bolum.setFixedHeight(40)
        self.spn_bolum.setFixedWidth(100)
        v_bolum.addWidget(self.spn_bolum)
        ctrl_layout.addLayout(v_bolum)

        # Dakika (kaldığı yer)
        v_dakika = QVBoxLayout()
        v_dakika.addWidget(QLabel("Kalinan Dakika:"))
        self.spn_dakika = QSpinBox()
        self.spn_dakika.setMinimum(0)
        self.spn_dakika.setMaximum(9999)
        self.spn_dakika.setSuffix(" dk")
        self.spn_dakika.setFixedHeight(40)
        self.spn_dakika.setFixedWidth(120)
        v_dakika.addWidget(self.spn_dakika)
        ctrl_layout.addLayout(v_dakika)

        # Toplam bölüm
        v_toplam = QVBoxLayout()
        v_toplam.addWidget(QLabel("Toplam Bolum:"))
        self.lbl_toplam_bolum = QLabel("1")
        self.lbl_toplam_bolum.setStyleSheet("font-size: 16px; color: #AAAAAA;")
        v_toplam.addWidget(self.lbl_toplam_bolum)
        ctrl_layout.addLayout(v_toplam)

        ctrl_layout.addStretch()
        layout.addWidget(controls)

        # Puan verme
        rating_grp = QGroupBox("Puan Ver (1-10)")
        rating_layout = QHBoxLayout(rating_grp)

        self.spn_puan = QSpinBox()
        self.spn_puan.setMinimum(1)
        self.spn_puan.setMaximum(10)
        self.spn_puan.setValue(7)
        self.spn_puan.setFixedHeight(40)
        self.spn_puan.setFixedWidth(80)
        rating_layout.addWidget(self.spn_puan)

        self.lbl_current_rating = QLabel("(Puan verilmemis)")
        self.lbl_current_rating.setStyleSheet("color: #AAAAAA;")
        rating_layout.addWidget(self.lbl_current_rating)
        rating_layout.addStretch()
        layout.addWidget(rating_grp)

        # Aksiyonlar
        actions = QHBoxLayout()
        actions.setSpacing(12)

        self.btn_save = QPushButton("Kaldigi Yere Kaydet")
        self.btn_save.setObjectName("btn_secondary")
        self.btn_save.setFixedHeight(44)
        self.btn_save.clicked.connect(lambda: self._save(tamamlandi=False))
        actions.addWidget(self.btn_save)

        self.btn_complete = QPushButton("Izlemeyi Tamamla")
        self.btn_complete.setFixedHeight(44)
        self.btn_complete.clicked.connect(lambda: self._save(tamamlandi=True))
        actions.addWidget(self.btn_complete)

        self.btn_rate = QPushButton("Puan Ver")
        self.btn_rate.setObjectName("btn_success")
        self.btn_rate.setFixedHeight(44)
        self.btn_rate.clicked.connect(self._do_rate)
        actions.addWidget(self.btn_rate)

        actions.addStretch()
        layout.addLayout(actions)

        # Mesaj
        self.lbl_msg = QLabel("")
        self.lbl_msg.setObjectName("lbl_success")
        layout.addWidget(self.lbl_msg)
        layout.addStretch()

    def load(self, program):
        """Dışarıdan program yükle ve mevcut pozisyona yerleş."""
        self._program = program
        uid = session.user_id

        self.lbl_title.setText(program.ad)
        self.lbl_toplam_bolum.setText(str(program.bolum_sayisi))
        self.spn_bolum.setMaximum(program.bolum_sayisi)
        self.lbl_msg.setText("")

        total_min = program.bolum_suresi or 0
        if total_min > 0:
            self._lbl_time_tot.setText(
                f"{total_min // 60:02d}:{total_min % 60:02d}"
            )
        else:
            self._lbl_time_tot.setText("--:--")

        if program.is_series:
            self.lbl_subtitle.setText(
                f"{program.program_tipi}  •  {program.bolum_sayisi} Bolum  •  "
                f"{program.bolum_suresi or '?'} dk/bolum"
            )
            self.spn_bolum.setEnabled(True)
        else:
            self.lbl_subtitle.setText(
                f"Film  •  {program.bolum_suresi or '?'} dakika"
            )
            self.spn_bolum.setValue(1)
            self.spn_bolum.setEnabled(False)

        # Mevcut pozisyonu yükle
        status = self._svc.get_watch_status(uid, program.program_id)
        if status:
            self.spn_bolum.setValue(status.son_bolum)
            self.spn_dakika.setValue(status.son_dakika)
            if status.puan:
                self.spn_puan.setValue(status.puan)
                self.lbl_current_rating.setText(
                    f"Mevcut puaniniz: {status.puan}/10"
                )
                self.lbl_current_rating.setStyleSheet("color: #E50914;")
            else:
                self.lbl_current_rating.setText("(Puan verilmemis)")
                self.lbl_current_rating.setStyleSheet("color: #AAAAAA;")

            cur = status.son_dakika
            self._lbl_time_cur.setText(f"{cur // 60:02d}:{cur % 60:02d}")
            if total_min > 0:
                self._progress_bar.setValue(min(100, int(cur * 100 / total_min)))

            if status.son_bolum > 1 or status.son_dakika > 0:
                self.lbl_screen_info.setText(
                    f"Bolum {status.son_bolum}, {status.son_dakika}. dakikadan devam ediliyor"
                )
            else:
                self.lbl_screen_info.setText("Oynatiliyor...")
        else:
            self.spn_bolum.setValue(1)
            self.spn_dakika.setValue(0)
            self._lbl_time_cur.setText("00:00")
            self._progress_bar.setValue(0)
            self.lbl_screen_info.setText("Oynatiliyor...")
            self.lbl_current_rating.setText("(Puan verilmemis)")

    def _save(self, tamamlandi: bool):
        if not self._program:
            return
        uid = session.user_id
        bolum = self.spn_bolum.value()
        dakika = self.spn_dakika.value()

        # Tamamlandı ama dakika girilmemişse bölüm/film süresini kullan
        if tamamlandi and dakika == 0 and self._program.bolum_suresi:
            dakika = self._program.bolum_suresi

        self._svc.save_progress(
            uid, self._program.program_id, bolum, dakika, tamamlandi
        )

        # Progress çubuğunu güncelle
        total_min = self._program.bolum_suresi or 0
        if total_min > 0:
            pct = 100 if tamamlandi else min(100, int(dakika * 100 / total_min))
            self._progress_bar.setValue(pct)
        self._lbl_time_cur.setText(f"{dakika // 60:02d}:{dakika % 60:02d}")

        if tamamlandi:
            self.lbl_msg.setText("Tebrikler! Izleme tamamlandi ve kaydedildi.")
            self.lbl_msg.setObjectName("lbl_success")
        else:
            self.lbl_msg.setText(
                f"Kaydedildi: Bolum {bolum}, {dakika}. dakika."
            )
        self.watch_saved.emit()

    def _do_rate(self):
        if not self._program:
            return
        puan = self.spn_puan.value()
        ok, msg = self._svc.rate(
            session.user_id, self._program.program_id, puan
        )
        if ok:
            self.lbl_current_rating.setText(f"Puaniniz guncellendi: {puan}/10")
            self.lbl_current_rating.setStyleSheet("color: #1DB954;")
            QMessageBox.information(self, "Basarili", f"Puaniniz: {puan}/10 olarak kaydedildi.")
        else:
            QMessageBox.warning(self, "Hata", msg)
