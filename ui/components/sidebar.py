from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QPushButton, QLabel,
                             QSpacerItem, QSizePolicy, QWidget)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class Sidebar(QFrame):
    page_changed     = pyqtSignal(int)
    logout_requested = pyqtSignal()

    def __init__(self, items: list[tuple[str, str]], is_admin=False):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(230)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Logo alani ────────────────────────────────────────────────
        logo_w = QWidget()
        logo_w.setFixedHeight(96)
        logo_w.setStyleSheet("background: transparent;")
        logo_l = QVBoxLayout(logo_w)
        logo_l.setContentsMargins(0, 16, 0, 12)
        logo_l.setSpacing(3)

        lbl_n = QLabel("N")
        lbl_n.setFont(QFont("Arial Black", 40, QFont.Weight.Bold))
        lbl_n.setStyleSheet(
            "color: #E50914; background: transparent; "
            "letter-spacing: -2px;"
        )
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_l.addWidget(lbl_n)

        sub_text = "YONETiCi" if is_admin else "PLATFORM"
        lbl_sub = QLabel(sub_text)
        lbl_sub.setStyleSheet(
            "color: #444444; font-size: 8px; font-weight: 700; "
            "letter-spacing: 4px; background: transparent;"
        )
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_l.addWidget(lbl_sub)

        layout.addWidget(logo_w)

        # Ince ayirici
        sep_top = QFrame()
        sep_top.setFixedHeight(1)
        sep_top.setStyleSheet("background: rgba(255,255,255,0.06);")
        layout.addWidget(sep_top)

        layout.addSpacing(8)

        # ── Navigasyon butonlari ──────────────────────────────────────
        self._buttons: list[QPushButton] = []
        for idx, (icon, text) in enumerate(items):
            btn = QPushButton(f"  {icon}   {text}")
            btn.setObjectName("sidebar_btn")
            btn.setCheckable(True)
            btn.setFixedHeight(52)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self._select(i))
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addSpacing(8)

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum,
                        QSizePolicy.Policy.Expanding)
        )

        # Ince ayirici
        sep_bot = QFrame()
        sep_bot.setFixedHeight(1)
        sep_bot.setStyleSheet("background: rgba(255,255,255,0.06);")
        layout.addWidget(sep_bot)

        # ── Cikis butonu ──────────────────────────────────────────────
        btn_logout = QPushButton("  ⎋   Cikis Yap")
        btn_logout.setObjectName("sidebar_logout")
        btn_logout.setFixedHeight(52)
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.logout_requested.emit)
        layout.addWidget(btn_logout)

        if self._buttons:
            self._select(0)

    def _select(self, index: int):
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)
        self.page_changed.emit(index)

    def select(self, index: int):
        self._select(index)
