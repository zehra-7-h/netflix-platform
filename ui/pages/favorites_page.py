from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QHeaderView, QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from services.content_service import ContentService
from repositories.genre_repository import GenreRepository
from utils.session import session


class FavoritesPage(QWidget):
    detail_requested = pyqtSignal(int)  # program_id

    def __init__(self):
        super().__init__()
        self._svc   = ContentService()
        self._genre = GenreRepository()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(16)

        lbl = QLabel("Favorilerim")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(lbl)

        # Filtre
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Ture Gore Filtrele:"))
        self.cmb_tur = QComboBox()
        self.cmb_tur.setFixedHeight(38)
        self.cmb_tur.setFixedWidth(220)
        self.cmb_tur.addItem("Tum Turler", 0)
        for t in self._genre.get_all():
            self.cmb_tur.addItem(t.tur_adi, t.tur_id)
        self.cmb_tur.currentIndexChanged.connect(self.refresh)
        filter_row.addWidget(self.cmb_tur)
        filter_row.addStretch()
        self.lbl_count = QLabel("")
        self.lbl_count.setStyleSheet("color: #AAAAAA;")
        filter_row.addWidget(self.lbl_count)
        layout.addLayout(filter_row)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Program Adi", "Tip", "Turler", "Ort. Puan", "Islemler"]
        )
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        hh.resizeSection(4, 220)
        hh.setStretchLastSection(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

    def refresh(self):
        tur_id = self.cmb_tur.currentData() or None
        favorites = self._svc.get_favorites(session.user_id, tur_id)
        self.lbl_count.setText(f"Toplam: {len(favorites)} favori")
        self.table.setRowCount(0)

        for fav in favorites:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(fav.program_adi or ""))
            self.table.setItem(row, 1, QTableWidgetItem(fav.program_tipi or ""))
            self.table.setItem(row, 2, QTableWidgetItem(fav.turler or ""))
            self.table.setItem(row, 3, QTableWidgetItem("–"))
            self.table.setRowHeight(row, 48)

            # Butonlar hücresi
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(6, 7, 6, 7)
            btn_layout.setSpacing(8)
            btn_layout.addStretch()

            btn_detail = QPushButton("→  Detay")
            btn_detail.setObjectName("btn_secondary")
            btn_detail.setFixedSize(98, 34)
            btn_detail.clicked.connect(
                lambda _, pid=fav.program_id: self.detail_requested.emit(pid)
            )
            btn_layout.addWidget(btn_detail)

            btn_remove = QPushButton("✕  Cikar")
            btn_remove.setObjectName("btn_danger")
            btn_remove.setFixedSize(88, 34)
            btn_remove.clicked.connect(
                lambda _, pid=fav.program_id: self._remove(pid)
            )
            btn_layout.addWidget(btn_remove)
            btn_layout.addStretch()
            self.table.setCellWidget(row, 4, btn_widget)

    def _remove(self, program_id: int):
        reply = QMessageBox.question(
            self, "Emin misiniz?",
            "Bu icerigi favorilerden cikarmak istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._svc.toggle_favorite(session.user_id, program_id)
            self.refresh()
