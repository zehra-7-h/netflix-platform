from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLineEdit, QComboBox, QSpinBox,
                             QFrame, QStackedWidget, QDoubleSpinBox,
                             QGroupBox, QScrollArea, QSizePolicy,
                             QAbstractSpinBox)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QPointF
from PyQt6.QtGui import QFont, QPainter, QColor, QPolygonF

from ui.components.sidebar import Sidebar
from ui.pages.content_detail_page import ContentDetailPage
from ui.pages.watch_page import WatchPage
from ui.pages.favorites_page import FavoritesPage
from ui.pages.watch_history_page import WatchHistoryPage
from ui.pages.profile_page import ProfilePage
from services.content_service import ContentService
from services.recommendation_service import RecommendationService
from repositories.genre_repository import GenreRepository
from utils.session import session


# ─────────────────────────────────────────────────────────────────────────────
# Alt sayfa: Kesfet / Browse
# ─────────────────────────────────────────────────────────────────────────────

class _VisibleSpinArrowsMixin:
    """Draws clear spinner arrows over the themed right-side button area."""

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#F7F7F7" if self.isEnabled() else "#777777"))

        panel_width = 30
        center_x = self.width() - panel_width / 2
        arrow_size = 5.5
        top_y = self.height() * 0.34
        bottom_y = self.height() * 0.66

        painter.drawPolygon(QPolygonF([
            QPointF(center_x, top_y - arrow_size / 2),
            QPointF(center_x - arrow_size, top_y + arrow_size / 2),
            QPointF(center_x + arrow_size, top_y + arrow_size / 2),
        ]))
        painter.drawPolygon(QPolygonF([
            QPointF(center_x, bottom_y + arrow_size / 2),
            QPointF(center_x - arrow_size, bottom_y - arrow_size / 2),
            QPointF(center_x + arrow_size, bottom_y - arrow_size / 2),
        ]))


class _VisibleArrowSpinBox(_VisibleSpinArrowsMixin, QSpinBox):
    pass


class _VisibleArrowDoubleSpinBox(_VisibleSpinArrowsMixin, QDoubleSpinBox):
    pass


class _BrowsePage(QWidget):
    detail_requested = pyqtSignal(int)   # program_id

    _TIPS = ["Tum Tipler", "Film", "Dizi", "Tv Show"]

    def __init__(self):
        super().__init__()
        self._svc       = ContentService()
        self._genre_rep = GenreRepository()
        self._rec_svc   = RecommendationService()
        self._programs  = []
        self._build_ui()

    # ── UI kurulum ────────────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        # Başlık
        header = QHBoxLayout()
        self._lbl_greeting = QLabel("Merhaba!")
        self._lbl_greeting.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.addWidget(self._lbl_greeting)
        header.addStretch()
        self._lbl_count = QLabel("")
        self._lbl_count.setStyleSheet("color: #AAAAAA; font-size: 13px;")
        header.addWidget(self._lbl_count)
        layout.addLayout(header)

        # Arama + filtre
        layout.addWidget(self._build_filter_row())

        # Öneriler (ince band)
        self._rec_frame = self._build_rec_frame()
        layout.addWidget(self._rec_frame)

        # İçerik tablosu
        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(
            ["Program Adi", "Tip", "Turler", "Yil", "Puan", "Izlenme"]
        )
        hh = self._table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        self._table.doubleClicked.connect(self._on_row_double_clicked)
        layout.addWidget(self._table)

        # Detay butonu (satır seçilince aktif)
        btn_row = QHBoxLayout()
        self._btn_detail = QPushButton("Detaya Git  →")
        self._btn_detail.setObjectName("btn_secondary")
        self._btn_detail.setFixedHeight(38)
        self._btn_detail.setFixedWidth(160)
        self._btn_detail.setEnabled(False)
        self._btn_detail.clicked.connect(self._on_detail_clicked)
        btn_row.addWidget(self._btn_detail)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self._table.selectionModel().selectionChanged.connect(
            lambda: self._btn_detail.setEnabled(
                len(self._table.selectedItems()) > 0
            )
        )

    def _build_filter_row(self) -> QFrame:
        frame = QFrame()
        row = QHBoxLayout(frame)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)

        self._inp_search = QLineEdit()
        self._inp_search.setPlaceholderText("Program ara...")
        self._inp_search.setFixedHeight(38)
        self._inp_search.returnPressed.connect(self.refresh)
        row.addWidget(self._inp_search, 2)

        self._cmb_tip = QComboBox()
        self._cmb_tip.setFixedHeight(38)
        self._cmb_tip.setFixedWidth(130)
        for tip in self._TIPS:
            self._cmb_tip.addItem(tip, "" if tip == "Tum Tipler" else tip)
        row.addWidget(self._cmb_tip)

        self._cmb_tur = QComboBox()
        self._cmb_tur.setFixedHeight(38)
        self._cmb_tur.setFixedWidth(160)
        self._cmb_tur.addItem("Tum Turler", 0)
        for t in self._genre_rep.get_all():
            self._cmb_tur.addItem(t.tur_adi, t.tur_id)
        row.addWidget(self._cmb_tur)

        self._spn_yil = _VisibleArrowSpinBox()
        self._spn_yil.setFixedHeight(38)
        self._spn_yil.setFixedWidth(138)
        self._spn_yil.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self._spn_yil.setRange(0, 2030)
        self._spn_yil.setSpecialValueText("Tum Yillar")
        self._spn_yil.setValue(0)
        row.addWidget(self._spn_yil)

        self._spn_puan = _VisibleArrowDoubleSpinBox()
        self._spn_puan.setFixedHeight(38)
        self._spn_puan.setFixedWidth(132)
        self._spn_puan.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self._spn_puan.setRange(0.0, 10.0)
        self._spn_puan.setSingleStep(0.5)
        self._spn_puan.setSpecialValueText("Min Puan")
        self._spn_puan.setValue(0.0)
        row.addWidget(self._spn_puan)

        btn_ara = QPushButton("Ara")
        btn_ara.setFixedHeight(38)
        btn_ara.setFixedWidth(72)
        btn_ara.clicked.connect(self.refresh)
        row.addWidget(btn_ara)

        btn_temizle = QPushButton("Temizle")
        btn_temizle.setObjectName("btn_secondary")
        btn_temizle.setFixedHeight(38)
        btn_temizle.setFixedWidth(88)
        btn_temizle.clicked.connect(self._clear_filters)
        row.addWidget(btn_temizle)

        return frame

    def _build_rec_frame(self) -> QGroupBox:
        grp = QGroupBox("Size Ozel Onerileri")
        grp.setMaximumHeight(110)
        inner = QVBoxLayout(grp)
        inner.setContentsMargins(12, 8, 12, 8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._rec_container = QWidget()
        self._rec_layout = QHBoxLayout(self._rec_container)
        self._rec_layout.setSpacing(8)
        self._rec_layout.setContentsMargins(0, 0, 0, 0)
        self._rec_layout.addStretch()

        scroll.setWidget(self._rec_container)
        inner.addWidget(scroll)
        return grp

    # ── Veri yükleme ──────────────────────────────────────────────────────────

    def refresh(self):
        user = session.current_user
        if user:
            self._lbl_greeting.setText(f"Merhaba, {user.ad}!")

        # Filtre değerleri
        q       = self._inp_search.text().strip() or None
        tip     = self._cmb_tip.currentData() or None
        tur_id  = self._cmb_tur.currentData() or None
        yil     = self._spn_yil.value() or None
        min_p   = self._spn_puan.value() or None

        self._programs = self._svc.search(
            ad=q, tur_id=tur_id, tipi=tip,
            yayin_yili=yil, min_puan=min_p
        )
        self._lbl_count.setText(f"{len(self._programs)} icerik")
        self._fill_table()
        self._load_recommendations()

    def _fill_table(self):
        self._table.setRowCount(0)
        for prog in self._programs:
            row = self._table.rowCount()
            self._table.insertRow(row)

            puan_str = (f"{prog.ortalama_puan:.1f}"
                        if prog.ortalama_puan and prog.ortalama_puan > 0 else "–")

            values = [
                prog.ad,
                prog.program_tipi or "",
                prog.tur_listesi or "",
                str(prog.yayin_yili) if prog.yayin_yili else "–",
                puan_str,
                str(prog.toplam_izlenme),
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setData(Qt.ItemDataRole.UserRole, prog.program_id)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter
                                      if col != 0 and col != 2
                                      else Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self._table.setItem(row, col, item)
            self._table.setRowHeight(row, 44)

    def _load_recommendations(self):
        # Oneri bandini tamamen temizle.
        while self._rec_layout.count():
            item = self._rec_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.deleteLater()

        try:
            recs = self._rec_svc.get_registration_recommendations(
                session.user_id
            )
        except Exception as exc:
            print(f"[RECOMMENDATION ERROR] {exc}")
            recs = []

        if not recs:
            lbl = QLabel("Favori turlerinize gore oneriler hazirlanamadi.")
            lbl.setStyleSheet("color: #666; font-size: 12px;")
            self._rec_layout.addWidget(lbl)
        else:
            for rec in recs:
                ad  = rec["ad"]
                pid = rec["program_id"]
                btn = QPushButton(ad[:28] + ("…" if len(ad) > 28 else ""))
                btn.setObjectName("btn_secondary")
                btn.setFixedHeight(30)
                btn.setToolTip(ad)
                btn.clicked.connect(
                    lambda _, _pid=pid: self.detail_requested.emit(_pid)
                )
                self._rec_layout.addWidget(btn)

        self._rec_layout.addStretch()

    # ── Yardımcılar ───────────────────────────────────────────────────────────

    def _clear_filters(self):
        self._inp_search.clear()
        self._cmb_tip.setCurrentIndex(0)
        self._cmb_tur.setCurrentIndex(0)
        self._spn_yil.setValue(0)
        self._spn_puan.setValue(0.0)
        self.refresh()

    def _current_program_id(self) -> int | None:
        rows = self._table.selectedItems()
        if not rows:
            return None
        return rows[0].data(Qt.ItemDataRole.UserRole)

    def _on_row_double_clicked(self, index):
        pid = self._table.item(index.row(), 0).data(Qt.ItemDataRole.UserRole)
        if pid:
            self.detail_requested.emit(pid)

    def _on_detail_clicked(self):
        pid = self._current_program_id()
        if pid:
            self.detail_requested.emit(pid)


# ─────────────────────────────────────────────────────────────────────────────
# Ana sayfa: Kullanici paneli
# ─────────────────────────────────────────────────────────────────────────────

class UserHomePage(QWidget):
    logout_requested = pyqtSignal()

    _NAV_ITEMS = [
        ("🏠", "Kesfet"),
        ("❤", "Favorilerim"),
        ("🕐", "Gecmisim"),
        ("👤", "Profilim"),
    ]

    # Stack indeksleri
    _IDX_BROWSE   = 0
    _IDX_FAVORITES = 1
    _IDX_HISTORY  = 2
    _IDX_PROFILE  = 3
    _IDX_DETAIL   = 4
    _IDX_WATCH    = 5

    def __init__(self):
        super().__init__()
        self._prev_main_idx = self._IDX_BROWSE  # detay/watch'tan dönünce
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────────────────────────
        self._sidebar = Sidebar(self._NAV_ITEMS, is_admin=False)
        self._sidebar.page_changed.connect(self._on_nav_changed)
        self._sidebar.logout_requested.connect(self.logout_requested)
        root.addWidget(self._sidebar)

        # ── İçerik alanı ──────────────────────────────────────────────────────
        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        # [0] Browse
        self._browse = _BrowsePage()
        self._browse.detail_requested.connect(self._show_detail)
        self._stack.addWidget(self._browse)

        # [1] Favoriler
        self._favorites = FavoritesPage()
        self._favorites.detail_requested.connect(self._show_detail)
        self._stack.addWidget(self._favorites)

        # [2] Gecmis
        self._history = WatchHistoryPage()
        self._stack.addWidget(self._history)

        # [3] Profil
        self._profile = ProfilePage()
        self._stack.addWidget(self._profile)

        # [4] Detay
        self._detail = ContentDetailPage()
        self._detail.back_requested.connect(self._back_from_detail)
        self._detail.watch_requested.connect(self._show_watch)
        self._stack.addWidget(self._detail)

        # [5] Izle
        self._watch = WatchPage()
        self._watch.back_requested.connect(self._back_from_watch)
        self._watch.watch_saved.connect(self._on_watch_saved)
        self._stack.addWidget(self._watch)

        self._stack.setCurrentIndex(self._IDX_BROWSE)

    # ── Navigasyon ────────────────────────────────────────────────────────────

    def _on_nav_changed(self, idx: int):
        """Sidebar butonuna basıldığında ilgili sayfayı yükle."""
        self._stack.setCurrentIndex(idx)
        if idx == self._IDX_BROWSE:
            self._browse.refresh()
        elif idx == self._IDX_FAVORITES:
            self._favorites.refresh()
        elif idx == self._IDX_HISTORY:
            self._history.refresh()
        elif idx == self._IDX_PROFILE:
            self._profile.refresh()

    def _show_detail(self, program_id: int):
        """İçerik detay sayfasına geç."""
        from services.content_service import ContentService
        prog = ContentService().get_by_id(program_id)
        if not prog:
            return
        self._prev_main_idx = self._stack.currentIndex()
        self._detail.load(prog)
        self._stack.setCurrentIndex(self._IDX_DETAIL)

    def _back_from_detail(self):
        """Detay sayfasından geri dön."""
        self._stack.setCurrentIndex(self._prev_main_idx)
        # Favori veya browse listesini yenile
        if self._prev_main_idx == self._IDX_FAVORITES:
            self._favorites.refresh()
        elif self._prev_main_idx == self._IDX_BROWSE:
            self._browse.refresh()

    def _show_watch(self, program):
        """İzleme sayfasına geç."""
        self._watch.load(program)
        self._stack.setCurrentIndex(self._IDX_WATCH)

    def _back_from_watch(self):
        """İzleme sayfasından detay sayfasına dön."""
        self._stack.setCurrentIndex(self._IDX_DETAIL)

    def _on_watch_saved(self):
        """İzleme kaydedildiğinde detay sayfasını yenile."""
        if self._detail._program:
            self._detail.load(self._detail._program)

    # ── Dışarıdan çağrılan ────────────────────────────────────────────────────

    def refresh(self):
        """MainWindow login sonrası çağırır."""
        self._sidebar.select(self._IDX_BROWSE)
        self._browse.refresh()
