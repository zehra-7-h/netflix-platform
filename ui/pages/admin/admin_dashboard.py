from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QStackedWidget, QDialog, QDialogButtonBox, QLineEdit,
    QComboBox, QSpinBox, QTextEdit, QGroupBox, QGridLayout,
    QTabWidget, QFrame, QScrollArea, QCheckBox, QSizePolicy,
    QInputDialog,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from ui.components.sidebar import Sidebar
from services.admin_service import AdminService
from repositories.genre_repository import GenreRepository


# ─────────────────────────────────────────────────────────────────────────────
# Program ekleme / düzenleme dialog
# ─────────────────────────────────────────────────────────────────────────────

class _ProgramDialog(QDialog):

    _TIPLER = ["Film", "Dizi", "Tv Show"]

    def __init__(self, genres, program=None, parent=None):
        super().__init__(parent)
        self._genres = genres
        self._program = program
        self.setWindowTitle("Program Ekle" if not program else "Program Duzenle")
        self.setMinimumWidth(520)
        self._build_ui()
        if program:
            self._fill(program)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        form = QGridLayout()
        form.setSpacing(10)

        def row(lbl_text, widget, r):
            lbl = QLabel(lbl_text)
            lbl.setStyleSheet("color:#AAAAAA;")
            form.addWidget(lbl, r, 0)
            form.addWidget(widget, r, 1)

        self.inp_ad = QLineEdit(); self.inp_ad.setFixedHeight(36)
        row("Ad *:", self.inp_ad, 0)

        self.cmb_tip = QComboBox(); self.cmb_tip.setFixedHeight(36)
        self.cmb_tip.addItems(self._TIPLER)
        self.cmb_tip.currentTextChanged.connect(self._on_tip_changed)
        row("Tip *:", self.cmb_tip, 1)

        self.spn_yil = QSpinBox()
        self.spn_yil.setRange(1900, 2030); self.spn_yil.setValue(2024)
        self.spn_yil.setFixedHeight(36)
        row("Yayin Yili:", self.spn_yil, 2)

        self.spn_bolum = QSpinBox()
        self.spn_bolum.setRange(1, 9999); self.spn_bolum.setValue(1)
        self.spn_bolum.setFixedHeight(36)
        row("Bolum Sayisi:", self.spn_bolum, 3)

        self.spn_sure = QSpinBox()
        self.spn_sure.setRange(1, 9999); self.spn_sure.setValue(90)
        self.spn_sure.setSuffix(" dk"); self.spn_sure.setFixedHeight(36)
        row("Bolum/Film Suresi:", self.spn_sure, 4)

        layout.addLayout(form)

        # Açıklama
        layout.addWidget(QLabel("Aciklama:"))
        self.txt_aciklama = QTextEdit()
        self.txt_aciklama.setMaximumHeight(80)
        layout.addWidget(self.txt_aciklama)

        # Türler
        grp_tur = QGroupBox("Turler (en az 1 secin)")
        tur_layout = QGridLayout(grp_tur)
        tur_layout.setSpacing(6)
        self._tur_checks: list[QCheckBox] = []
        for i, g in enumerate(self._genres):
            cb = QCheckBox(g.tur_adi)
            cb.setProperty("tur_id", g.tur_id)
            self._tur_checks.append(cb)
            tur_layout.addWidget(cb, i // 4, i % 4)
        layout.addWidget(grp_tur)

        # Butonlar
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._validate_and_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        self._on_tip_changed(self.cmb_tip.currentText())

    def _on_tip_changed(self, tip: str):
        is_movie = (tip == "Film")
        self.spn_bolum.setEnabled(not is_movie)
        if is_movie:
            self.spn_bolum.setValue(1)

    def _fill(self, prog):
        self.inp_ad.setText(prog.ad)
        idx = self.cmb_tip.findText(prog.program_tipi)
        if idx >= 0:
            self.cmb_tip.setCurrentIndex(idx)
        if prog.yayin_yili:
            self.spn_yil.setValue(prog.yayin_yili)
        self.spn_bolum.setValue(prog.bolum_sayisi or 1)
        if prog.bolum_suresi:
            self.spn_sure.setValue(prog.bolum_suresi)
        self.txt_aciklama.setPlainText(prog.aciklama or "")

        # Tür seçimleri
        tur_ids = {int(t) for t in (prog.tur_listesi or "").split(",") if t.strip().isdigit()}
        # tur_listesi = tur isimleri virgülle ayrılmış; id'leri doğrudan alamayız
        # _genres ile eşleştirme yapalım
        tur_adlari = {t.strip() for t in (prog.tur_listesi or "").split(",")}
        for cb in self._tur_checks:
            if cb.text() in tur_adlari:
                cb.setChecked(True)

    def _validate_and_accept(self):
        if not self.inp_ad.text().strip():
            QMessageBox.warning(self, "Hata", "Program adi bos birakilamaz.")
            return
        if not self.selected_tur_ids():
            QMessageBox.warning(self, "Hata", "En az bir tur secmelisiniz.")
            return
        self.accept()

    def values(self) -> dict:
        return {
            "ad": self.inp_ad.text().strip(),
            "program_tipi": self.cmb_tip.currentText(),
            "yayin_yili": self.spn_yil.value(),
            "bolum_sayisi": self.spn_bolum.value(),
            "bolum_suresi": self.spn_sure.value(),
            "aciklama": self.txt_aciklama.toPlainText().strip(),
            "tur_idler": self.selected_tur_ids(),
        }

    def selected_tur_ids(self) -> list[int]:
        return [cb.property("tur_id") for cb in self._tur_checks if cb.isChecked()]


# ─────────────────────────────────────────────────────────────────────────────
# İçerik yönetim sayfası
# ─────────────────────────────────────────────────────────────────────────────

class _ContentPage(QWidget):

    def __init__(self, svc: AdminService):
        super().__init__()
        self._svc = svc
        self._genre_rep = GenreRepository()
        self._programs = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        header = QHBoxLayout()
        lbl = QLabel("Icerik Yonetimi")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.addWidget(lbl)
        header.addStretch()

        self._lbl_count = QLabel("")
        self._lbl_count.setStyleSheet("color:#AAAAAA;")
        header.addWidget(self._lbl_count)

        btn_add = QPushButton("+ Yeni Program")
        btn_add.setFixedHeight(38)
        btn_add.setFixedWidth(150)
        btn_add.clicked.connect(self._add_program)
        header.addWidget(btn_add)
        layout.addLayout(header)

        # Arama satırı
        search_row = QHBoxLayout()
        self._inp_search = QLineEdit()
        self._inp_search.setPlaceholderText("Program ara...")
        self._inp_search.setFixedHeight(36)
        self._inp_search.returnPressed.connect(self.refresh)
        search_row.addWidget(self._inp_search)

        btn_ara = QPushButton("Ara")
        btn_ara.setFixedHeight(36); btn_ara.setFixedWidth(72)
        btn_ara.clicked.connect(self.refresh)
        search_row.addWidget(btn_ara)

        btn_tm = QPushButton("Tumunu Goster")
        btn_tm.setObjectName("btn_secondary")
        btn_tm.setFixedHeight(36); btn_tm.setFixedWidth(140)
        btn_tm.clicked.connect(lambda: (self._inp_search.clear(), self.refresh()))
        search_row.addWidget(btn_tm)
        layout.addLayout(search_row)

        # Tablo
        self._table = QTableWidget()
        self._table.setColumnCount(7)
        self._table.setHorizontalHeaderLabels(
            ["Ad", "Tip", "Turler", "Yil", "Bolum", "Puan", "Islemler"]
        )
        hh = self._table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        hh.resizeSection(6, 200)
        hh.setStretchLastSection(False)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        layout.addWidget(self._table)

    def refresh(self):
        from services.content_service import ContentService
        svc = ContentService()
        q = self._inp_search.text().strip() or None
        self._programs = svc.search(ad=q) if q else svc.get_all()
        self._lbl_count.setText(f"Toplam: {len(self._programs)} icerik")
        self._fill_table()

    def _fill_table(self):
        self._table.setRowCount(0)
        for prog in self._programs:
            row = self._table.rowCount()
            self._table.insertRow(row)
            puan = f"{prog.ortalama_puan:.1f}" if prog.ortalama_puan > 0 else "–"
            values = [
                prog.ad, prog.program_tipi or "",
                prog.tur_listesi or "",
                str(prog.yayin_yili) if prog.yayin_yili else "–",
                str(prog.bolum_sayisi),
                puan,
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole, prog.program_id)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter
                                      if col not in (0, 2)
                                      else Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self._table.setItem(row, col, item)

            # Butonlar
            btn_w = QWidget()
            btn_l = QHBoxLayout(btn_w)
            btn_l.setContentsMargins(6, 8, 6, 8)
            btn_l.setSpacing(6)
            btn_l.addStretch()

            btn_edit = QPushButton("Duzenle")
            btn_edit.setObjectName("btn_secondary")
            btn_edit.setFixedSize(82, 30)
            btn_edit.clicked.connect(lambda _, p=prog: self._edit_program(p))
            btn_l.addWidget(btn_edit)

            btn_del = QPushButton("Sil")
            btn_del.setObjectName("btn_danger")
            btn_del.setFixedSize(55, 30)
            btn_del.clicked.connect(lambda _, pid=prog.program_id: self._delete_program(pid))
            btn_l.addWidget(btn_del)

            btn_l.addStretch()
            self._table.setCellWidget(row, 6, btn_w)
            self._table.setRowHeight(row, 46)

    def _genres(self):
        return self._genre_rep.get_all()

    def _add_program(self):
        dlg = _ProgramDialog(self._genres(), parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            v = dlg.values()
            ok, msg = self._svc.add_program(
                v["ad"], v["aciklama"], v["program_tipi"],
                v["yayin_yili"], v["bolum_sayisi"], v["bolum_suresi"],
                v["tur_idler"]
            )
            if ok:
                QMessageBox.information(self, "Basarili", "Program eklendi.")
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)

    def _edit_program(self, prog):
        dlg = _ProgramDialog(self._genres(), program=prog, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            v = dlg.values()
            ok, msg = self._svc.update_program(
                prog.program_id, v["ad"], v["aciklama"], v["program_tipi"],
                v["yayin_yili"], v["bolum_sayisi"], v["bolum_suresi"],
                v["tur_idler"]
            )
            if ok:
                QMessageBox.information(self, "Basarili", "Program guncellendi.")
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)

    def _delete_program(self, program_id: int):
        reply = QMessageBox.question(
            self, "Emin misiniz?",
            "Bu programi silmek istediginizden emin misiniz?\n"
            "Ilgili tum izleme gecmisi de silinecektir.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, msg = self._svc.delete_program(program_id)
            if ok:
                QMessageBox.information(self, "Silindi", "Program silindi.")
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)


# ─────────────────────────────────────────────────────────────────────────────
# Tür yönetim sayfası
# ─────────────────────────────────────────────────────────────────────────────

class _GenrePage(QWidget):

    def __init__(self, svc: AdminService):
        super().__init__()
        self._svc = svc
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        header = QHBoxLayout()
        lbl = QLabel("Tur Yonetimi")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.addWidget(lbl)
        header.addStretch()
        btn_add = QPushButton("+ Yeni Tur")
        btn_add.setFixedHeight(38); btn_add.setFixedWidth(130)
        btn_add.clicked.connect(self._add_genre)
        header.addWidget(btn_add)
        layout.addLayout(header)

        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["ID", "Tur Adi", "Islemler"])
        hh = self._table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        hh.resizeSection(2, 200)
        hh.setStretchLastSection(False)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        layout.addWidget(self._table)

    def refresh(self):
        genres = GenreRepository().get_all()
        self._table.setRowCount(0)
        for g in genres:
            row = self._table.rowCount()
            self._table.insertRow(row)
            self._table.setItem(row, 0, QTableWidgetItem(str(g.tur_id)))
            item = QTableWidgetItem(g.tur_adi)
            item.setData(Qt.ItemDataRole.UserRole, g.tur_id)
            self._table.setItem(row, 1, item)

            btn_w = QWidget()
            btn_l = QHBoxLayout(btn_w)
            btn_l.setContentsMargins(6, 7, 6, 7)
            btn_l.setSpacing(6)
            btn_l.addStretch()

            btn_edit = QPushButton("Duzenle")
            btn_edit.setObjectName("btn_secondary")
            btn_edit.setFixedSize(82, 30)
            btn_edit.clicked.connect(lambda _, g=g: self._edit_genre(g))
            btn_l.addWidget(btn_edit)

            btn_del = QPushButton("Sil")
            btn_del.setObjectName("btn_danger")
            btn_del.setFixedSize(55, 30)
            btn_del.clicked.connect(lambda _, tid=g.tur_id: self._delete_genre(tid))
            btn_l.addWidget(btn_del)

            btn_l.addStretch()
            self._table.setCellWidget(row, 2, btn_w)
            self._table.setRowHeight(row, 44)

    def _add_genre(self):
        text, ok = QInputDialog.getText(self, "Yeni Tur", "Tur adi:")
        if ok and text.strip():
            res_ok, msg = self._svc.add_genre(text.strip())
            if res_ok:
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)

    def _edit_genre(self, genre):
        text, ok = QInputDialog.getText(
            self, "Tur Duzenle", "Yeni tur adi:", text=genre.tur_adi
        )
        if ok and text.strip():
            res_ok, msg = self._svc.update_genre(genre.tur_id, text.strip())
            if res_ok:
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)

    def _delete_genre(self, tur_id: int):
        reply = QMessageBox.question(
            self, "Emin misiniz?", "Bu turu silmek istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, msg = self._svc.delete_genre(tur_id)
            if ok:
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)


# ─────────────────────────────────────────────────────────────────────────────
# Kullanıcı yönetim sayfası
# ─────────────────────────────────────────────────────────────────────────────

class _UserPage(QWidget):

    def __init__(self, svc: AdminService):
        super().__init__()
        self._svc = svc
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        lbl = QLabel("Kullanici Yonetimi")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(lbl)

        self._lbl_count = QLabel("")
        self._lbl_count.setStyleSheet("color:#AAAAAA;")
        layout.addWidget(self._lbl_count)

        self._table = QTableWidget()
        self._table.setColumnCount(7)
        self._table.setHorizontalHeaderLabels([
            "Ad Soyad", "E-mail", "Kayit Tarihi",
            "Cinsiyet", "Ulke", "Durum", "Islemler"
        ])
        hh = self._table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        hh.resizeSection(6, 240)
        hh.setStretchLastSection(False)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        layout.addWidget(self._table)

    def refresh(self):
        users = self._svc.get_all_users()
        aktif_count = sum(1 for u in users if u.aktif)
        self._lbl_count.setText(
            f"Toplam {len(users)} kullanici  |  {aktif_count} aktif"
        )
        self._table.setRowCount(0)
        for user in users:
            row = self._table.rowCount()
            self._table.insertRow(row)

            kayit = (user.kayit_tarihi.strftime("%d.%m.%Y")
                     if user.kayit_tarihi else "–")
            durum = "Aktif" if user.aktif else "Pasif"

            values = [
                f"{user.ad} {user.soyad}",
                user.email,
                kayit,
                user.cinsiyet or "–",
                user.ulke or "–",
                durum,
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole, user.kullanici_id)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter
                                      if col not in (0, 1)
                                      else Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if col == 5:
                    item.setForeground(
                        Qt.GlobalColor.green if user.aktif else Qt.GlobalColor.gray
                    )
                self._table.setItem(row, col, item)

            btn_w = QWidget()
            btn_l = QHBoxLayout(btn_w)
            btn_l.setContentsMargins(6, 8, 6, 8)
            btn_l.setSpacing(6)
            btn_l.addStretch()

            lbl_toggle = "Pasif Yap" if user.aktif else "Aktif Yap"
            obj_name = "btn_danger" if user.aktif else "btn_success"
            btn_toggle = QPushButton(lbl_toggle)
            btn_toggle.setObjectName(obj_name)
            btn_toggle.setFixedSize(100, 30)
            btn_toggle.clicked.connect(
                lambda _, uid=user.kullanici_id, a=user.aktif: self._toggle(uid, a)
            )
            btn_l.addWidget(btn_toggle)

            btn_stat = QPushButton("Istatistik")
            btn_stat.setObjectName("btn_secondary")
            btn_stat.setFixedSize(112, 30)
            btn_stat.clicked.connect(
                lambda _, uid=user.kullanici_id,
                       nm=f"{user.ad} {user.soyad}": self._show_stats(uid, nm)
            )
            btn_l.addWidget(btn_stat)

            btn_l.addStretch()
            self._table.setCellWidget(row, 6, btn_w)
            self._table.setRowHeight(row, 46)

    def _toggle(self, uid: int, currently_active: bool):
        action = "pasif" if currently_active else "aktif"
        reply = QMessageBox.question(
            self, "Emin misiniz?",
            f"Kullaniciyi {action} yapmak istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, msg = self._svc.set_user_active(uid, not currently_active)
            if ok:
                self.refresh()
            else:
                QMessageBox.warning(self, "Hata", msg)

    def _show_stats(self, uid: int, name: str):
        stats = self._svc.get_user_stats(uid)
        QMessageBox.information(
            self, f"{name} - Istatistikler",
            f"Izlenen Icerik: {stats.get('izlenen_icerik', 0)}\n"
            f"Toplam Sure: {stats.get('toplam_dakika', 0)} dakika\n"
            f"Ortalama Puan: "
            + (f"{stats['ort_puan']:.1f}" if stats.get('ort_puan') else "–")
        )


# ─────────────────────────────────────────────────────────────────────────────
# Raporlar sayfası
# ─────────────────────────────────────────────────────────────────────────────

class _ReportPage(QWidget):

    def __init__(self, svc: AdminService):
        super().__init__()
        self._svc = svc
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        header = QHBoxLayout()
        lbl = QLabel("Raporlar")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.addWidget(lbl)
        header.addStretch()
        btn_ref = QPushButton("Yenile")
        btn_ref.setObjectName("btn_secondary")
        btn_ref.setFixedHeight(36); btn_ref.setFixedWidth(90)
        btn_ref.clicked.connect(self.refresh)
        header.addWidget(btn_ref)
        layout.addLayout(header)

        # Özet kartlar
        self._summary_frame = QFrame()
        self._summary_frame.setObjectName("stat_card")
        self._sum_layout = QHBoxLayout(self._summary_frame)
        self._sum_layout.setSpacing(40)
        self._sum_layout.setContentsMargins(24, 16, 24, 16)

        self._lbl_k  = self._stat(self._sum_layout, "Aktif Kullanici", "–")
        self._lbl_i  = self._stat(self._sum_layout, "Toplam Izlenme", "–")
        self._lbl_p  = self._stat(self._sum_layout, "Verilen Puan", "–")
        self._lbl_ic = self._stat(self._sum_layout, "Toplam Icerik", "–")
        self._sum_layout.addStretch()
        layout.addWidget(self._summary_frame)

        # Sekmeli raporlar
        self._tabs = QTabWidget()
        layout.addWidget(self._tabs)

        self._tbl_top_w  = self._make_table(["Program", "Tip", "Izlenme", "Puan"])
        self._tbl_top_r  = self._make_table(["Program", "Tip", "Puan", "Izlenme"])
        self._tbl_genres = self._make_table(["Tur", "Toplam Izlenme"])
        self._tbl_genres.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self._tbl_users  = self._make_table(["Ad Soyad", "Email", "Izlenen", "Toplam Dk"])
        self._tbl_7day   = self._make_table(["Program", "Tip", "Izlenme", "Son Tarih"])

        self._tabs.addTab(self._wrap(self._tbl_top_w),  "En Cok Izlenen")
        self._tabs.addTab(self._wrap(self._tbl_top_r),  "En Yuksek Puan")
        self._tabs.addTab(self._wrap(self._tbl_genres), "Populer Turler")
        self._tabs.addTab(self._wrap(self._tbl_users),  "En Aktif Kullanicilar")
        self._tabs.addTab(self._wrap(self._tbl_7day),   "Son 7 Gun")

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

    def _make_table(self, headers: list[str]) -> QTableWidget:
        t = QTableWidget()
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setAlternatingRowColors(True)
        t.verticalHeader().setVisible(False)
        t.setShowGrid(False)
        return t

    def _wrap(self, widget: QWidget) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 8, 0, 0)
        l.addWidget(widget)
        return w

    def _fill_table(self, table: QTableWidget, rows: list[list]):
        table.setRowCount(0)
        for values in rows:
            row = table.rowCount()
            table.insertRow(row)
            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter
                                      if col > 0
                                      else Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                table.setItem(row, col, item)
            table.setRowHeight(row, 40)

    def refresh(self):
        summary = self._svc.summary()
        self._lbl_k.setText(str(summary["kullanici_sayisi"]))
        self._lbl_i.setText(str(summary["toplam_izlenme"]))
        self._lbl_p.setText(str(summary["toplam_puan"]))
        self._lbl_ic.setText(str(summary["toplam_icerik"]))

        self._fill_table(self._tbl_top_w, [
            [r["ad"], r["tip"], r["izlenme"], f"{r['puan']:.1f}" if r["puan"] else "–"]
            for r in self._svc.top_watched()
        ])
        self._fill_table(self._tbl_top_r, [
            [r["ad"], r["tip"], f"{r['puan']:.1f}", r["izlenme"]]
            for r in self._svc.top_rated()
        ])
        self._fill_table(self._tbl_genres, [
            [r["tur"], r["izlenme"]] for r in self._svc.top_genres()
        ])
        self._fill_table(self._tbl_users, [
            [r["isim"], r["email"], r["icerik_sayisi"], r["toplam_dakika"]]
            for r in self._svc.most_active_users()
        ])
        self._fill_table(self._tbl_7day, [
            [r["ad"], r["tip"], r["izlenme"],
             r["son"].strftime("%d.%m.%Y") if r.get("son") else "–"]
            for r in self._svc.last_7_days()
        ])


# ─────────────────────────────────────────────────────────────────────────────
# Admin ana sayfa
# ─────────────────────────────────────────────────────────────────────────────

class AdminDashboard(QWidget):
    logout_requested = pyqtSignal()

    _NAV_ITEMS = [
        ("🎬", "Icerikler"),
        ("🏷", "Turler"),
        ("👥", "Kullanicilar"),
        ("📊", "Raporlar"),
    ]

    def __init__(self):
        super().__init__()
        self._svc = AdminService()
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._sidebar = Sidebar(self._NAV_ITEMS, is_admin=True)
        self._sidebar.page_changed.connect(self._on_nav)
        self._sidebar.logout_requested.connect(self.logout_requested)
        root.addWidget(self._sidebar)

        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        self._content_page = _ContentPage(self._svc)
        self._genre_page   = _GenrePage(self._svc)
        self._user_page    = _UserPage(self._svc)
        self._report_page  = _ReportPage(self._svc)

        for page in [self._content_page, self._genre_page,
                     self._user_page, self._report_page]:
            self._stack.addWidget(page)

        self._stack.setCurrentIndex(0)

    def _on_nav(self, idx: int):
        self._stack.setCurrentIndex(idx)
        pages = [self._content_page, self._genre_page,
                 self._user_page, self._report_page]
        pages[idx].refresh()

    def refresh(self):
        self._sidebar.select(0)
        self._content_page.refresh()
