from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from services.content_service import ContentService
from utils.session import session


class WatchHistoryPage(QWidget):

    def __init__(self):
        super().__init__()
        self._svc = ContentService()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(16)

        lbl = QLabel("Izleme Gecmisim")
        lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(lbl)

        self.lbl_count = QLabel("")
        self.lbl_count.setStyleSheet("color: #AAAAAA;")
        layout.addWidget(self.lbl_count)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Program Adi", "Tip", "Izleme Tarihi",
            "Izlenen Bolum", "Sure (dk)", "Puan", "Tamamlandi"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

    def refresh(self):
        logs = self._svc.get_watch_history(session.user_id)
        self.lbl_count.setText(f"Toplam {len(logs)} izleme kaydi")
        self.table.setRowCount(0)

        for log in logs:
            row = self.table.rowCount()
            self.table.insertRow(row)

            tarih = (log.izleme_tarihi.strftime("%d.%m.%Y %H:%M")
                     if log.izleme_tarihi else "–")
            tam = "Evet" if log.tamamlandi else "Hayir"

            values = [
                log.program_adi or "",
                log.program_tipi or "",
                tarih,
                str(log.izlenen_bolum),
                str(log.izleme_suresi),
                "–",
                tam,
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 6:
                    item.setForeground(
                        Qt.GlobalColor.green if log.tamamlandi
                        else Qt.GlobalColor.gray
                    )
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, 44)
