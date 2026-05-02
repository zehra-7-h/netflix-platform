from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QHeaderView,
    QMessageBox,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from services.content_service import ContentService
from repositories.genre_repository import GenreRepository
from utils.session import session


class FavoritesPage(QWidget):
    detail_requested = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._svc = ContentService()
        self._genre = GenreRepository()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(16)

        lbl = QLabel("Favorilerim")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(lbl)

        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Ture Gore Filtrele:"))

        self.cmb_tur = QComboBox()
        self.cmb_tur.setFixedHeight(38)
        self.cmb_tur.setFixedWidth(220)
        self.cmb_tur.addItem("Tum Turler", 0)
        for genre in self._genre.get_all():
            self.cmb_tur.addItem(genre.tur_adi, genre.tur_id)
        self.cmb_tur.currentIndexChanged.connect(self.refresh)
        filter_row.addWidget(self.cmb_tur)

        filter_row.addStretch()

        self.lbl_count = QLabel("")
        self.lbl_count.setStyleSheet("color: #AAAAAA;")
        filter_row.addWidget(self.lbl_count)
        layout.addLayout(filter_row)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Program Adi", "Tip", "Turler", "Ort. Puan", "Islemler"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 250)
        header.setStretchLastSection(False)

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

            values = [
                fav.program_adi or "",
                fav.program_tipi or "",
                fav.turler or "",
                "-",
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                    if col in (1, 3)
                    else Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
                )
                self.table.setItem(row, col, item)

            self.table.setRowHeight(row, 56)
            self.table.setCellWidget(row, 4, self._build_actions(fav.program_id))

    def _build_actions(self, program_id: int) -> QWidget:
        container = QWidget()
        container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_detail = QPushButton("Detay")
        btn_detail.setObjectName("btn_table_secondary")
        btn_detail.setFixedSize(104, 34)
        btn_detail.clicked.connect(
            lambda _, pid=program_id: self.detail_requested.emit(pid)
        )
        layout.addWidget(btn_detail)

        btn_remove = QPushButton("Cikar")
        btn_remove.setObjectName("btn_table_danger")
        btn_remove.setFixedSize(104, 34)
        btn_remove.clicked.connect(lambda _, pid=program_id: self._remove(pid))
        layout.addWidget(btn_remove)

        outer.addStretch(1)
        outer.addLayout(layout)
        outer.addStretch(1)
        return container

    def _remove(self, program_id: int):
        reply = QMessageBox.question(
            self,
            "Emin misiniz?",
            "Bu icerigi favorilerden cikarmak istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._svc.toggle_favorite(session.user_id, program_id)
            self.refresh()
