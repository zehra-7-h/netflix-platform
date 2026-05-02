DARK_THEME = """

/* ═══════════════════════════════════════════════════════════════════
   Netflix Platform — Premium Dark Theme
   Katmanli karanlik: #0D0D0D → #111 → #161616 → rgba card
   ═══════════════════════════════════════════════════════════════════ */

/* ── Global ─────────────────────────────────────────────────────── */
QWidget {
    background-color: #111111;
    color: #F0F0F0;
    font-family: 'Inter', 'Segoe UI', 'Roboto', 'Poppins', Arial, sans-serif;
    font-size: 13px;
    selection-background-color: #E50914;
    selection-color: #FFFFFF;
}
QMainWindow { background-color: #0D0D0D; }

/* ── Butonlar ───────────────────────────────────────────────────── */
QPushButton {
    background-color: #E50914;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 11px 22px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.4px;
    min-width: 72px;
}
QPushButton:hover {
    background-color: #FF1A24;
}
QPushButton:pressed {
    background-color: #A8000C;
    padding-top: 12px;
    padding-bottom: 10px;
}
QPushButton:disabled {
    background-color: #2A2A2A;
    color: #606060;
    border: 1px solid #333333;
}

QPushButton#btn_secondary {
    background-color: #2D2D2D;
    color: #DDDDDD;
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 7px 10px;
}
QPushButton#btn_secondary:hover {
    background-color: #3A3A3A;
    border-color: rgba(255, 255, 255, 0.24);
    color: #FFFFFF;
}
QPushButton#btn_secondary:pressed {
    background-color: #222222;
}

QPushButton#btn_danger {
    background-color: #6B0000;
    border: 1px solid #8B0000;
    color: #FFAAAA;
    padding: 7px 8px;
}
QPushButton#btn_danger:hover {
    background-color: #8B0000;
    color: #FFFFFF;
}

QPushButton#btn_success {
    background-color: #1A8F3F;
    color: #FFFFFF;
    border-radius: 8px;
    padding: 7px 8px;
}
QPushButton#btn_success:hover { background-color: #1DB954; }
QPushButton#btn_success:pressed { background-color: #138030; }

/* ── Input Alanlari — yari transparan, Netflix stili ────────────── */
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.11);
    border-radius: 8px;
    padding: 10px 14px;
    color: #F5F5F5;
    font-size: 13px;
    min-height: 18px;
}
QLineEdit:hover, QComboBox:hover,
QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: rgba(255, 255, 255, 0.22);
    background-color: rgba(255, 255, 255, 0.07);
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus,
QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid rgba(229, 9, 20, 0.75);
    background-color: rgba(229, 9, 20, 0.05);
    padding: 9px 13px;
}
QLineEdit:read-only {
    background-color: rgba(255, 255, 255, 0.02);
    color: #707070;
    border-color: rgba(255, 255, 255, 0.06);
}

QComboBox::drop-down {
    border: none;
    padding-right: 12px;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #1E1E1E;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    selection-background-color: #E50914;
    selection-color: #FFFFFF;
    outline: none;
    padding: 4px;
}
QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    min-height: 28px;
    border-radius: 4px;
    margin: 1px 3px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: rgba(255, 255, 255, 0.08);
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    background-color: rgba(255, 255, 255, 0.09);
    border: none;
    border-left: 1px solid rgba(255, 255, 255, 0.12);
    border-top-right-radius: 7px;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    background-color: rgba(255, 255, 255, 0.09);
    border: none;
    border-left: 1px solid rgba(255, 255, 255, 0.12);
    border-bottom-right-radius: 7px;
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: rgba(255, 255, 255, 0.22);
}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {
    background-color: rgba(229, 9, 20, 0.30);
}

/* ── Tablolar — Modern List gorunumu ────────────────────────────── */
QTableWidget {
    background-color: transparent;
    border: none;
    gridline-color: transparent;
    alternate-background-color: rgba(255, 255, 255, 0.018);
    outline: none;
    border-radius: 10px;
}
QTableWidget::item {
    padding: 10px 14px;
    border: none;
    color: #E0E0E0;
}
QTableWidget::item:hover {
    background-color: rgba(255, 255, 255, 0.06);
    color: #FFFFFF;
}
QTableWidget::item:selected {
    background-color: rgba(229, 9, 20, 0.28);
    color: #FFFFFF;
}
QTableWidget::item:selected:hover {
    background-color: rgba(229, 9, 20, 0.38);
}
QHeaderView {
    background-color: transparent;
}
QHeaderView::section {
    background-color: rgba(255, 255, 255, 0.03);
    color: #808080;
    padding: 11px 14px;
    border: none;
    border-bottom: 1px solid rgba(229, 9, 20, 0.50);
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}
QHeaderView::section:hover {
    background-color: rgba(255, 255, 255, 0.06);
    color: #AAAAAA;
}

/* ── Etiketler ──────────────────────────────────────────────────── */
QLabel { color: #E8E8E8; background-color: transparent; }
QLabel#lbl_title {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 0.3px;
}
QLabel#lbl_subtitle {
    font-size: 13px;
    color: #909090;
}
QLabel#lbl_error {
    color: #FF5555;
    font-size: 12px;
    font-weight: 500;
}
QLabel#lbl_success {
    color: #1DB954;
    font-size: 12px;
    font-weight: 500;
}
QLabel#lbl_section {
    font-size: 17px;
    font-weight: 700;
    color: #FFFFFF;
}

/* ── Kaydirma Cubugu — ince ve elegan ───────────────────────────── */
QScrollBar:vertical {
    background-color: transparent;
    width: 6px;
    border-radius: 3px;
    margin: 2px 0;
}
QScrollBar::handle:vertical {
    background-color: rgba(255, 255, 255, 0.20);
    border-radius: 3px;
    min-height: 36px;
}
QScrollBar::handle:vertical:hover {
    background-color: rgba(255, 255, 255, 0.40);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 6px;
    border-radius: 3px;
    margin: 0 2px;
}
QScrollBar::handle:horizontal {
    background-color: rgba(255, 255, 255, 0.20);
    border-radius: 3px;
    min-width: 36px;
}
QScrollBar::handle:horizontal:hover {
    background-color: rgba(255, 255, 255, 0.40);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Sidebar — Glow efektli navigasyon ──────────────────────────── */
QFrame#sidebar {
    background-color: #0A0A0A;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

QPushButton#sidebar_btn {
    background-color: transparent;
    color: #808080;
    text-align: left;
    padding: 14px 20px;
    border-radius: 0px;
    border-left: 4px solid transparent;
    font-size: 13px;
    font-weight: 400;
    min-width: 0px;
    letter-spacing: 0.2px;
}
QPushButton#sidebar_btn:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #EEEEEE;
    border-left: 4px solid rgba(255, 255, 255, 0.20);
}
QPushButton#sidebar_btn:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0   rgba(229, 9, 20, 0.28),
        stop:0.5 rgba(229, 9, 20, 0.08),
        stop:1   rgba(229, 9, 20, 0.00));
    color: #FFFFFF;
    font-weight: 700;
    border-left: 4px solid #E50914;
    padding-left: 16px;
}

QPushButton#sidebar_logout {
    background-color: transparent;
    color: #994444;
    text-align: left;
    padding: 14px 20px;
    border-radius: 0px;
    border-left: 4px solid transparent;
    font-size: 13px;
    font-weight: 400;
    min-width: 0px;
}
QPushButton#sidebar_logout:hover {
    background-color: rgba(229, 9, 20, 0.08);
    color: #FF7777;
    border-left: 4px solid rgba(229, 9, 20, 0.40);
}

/* ── Kartlar — Glassmorphism katmanlama ─────────────────────────── */
QFrame#content_card {
    background-color: rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.09);
}
QFrame#content_card:hover {
    border-color: rgba(255, 255, 255, 0.18);
    background-color: rgba(255, 255, 255, 0.06);
}

QFrame#stat_card {
    background-color: rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* ── Sekmeler ───────────────────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid rgba(255, 255, 255, 0.08);
    background-color: #111111;
    border-top: none;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
QTabBar {
    background-color: transparent;
}
QTabBar::tab {
    background-color: transparent;
    color: #707070;
    padding: 11px 26px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
    font-weight: 500;
    min-width: 90px;
}
QTabBar::tab:selected {
    color: #FFFFFF;
    font-weight: 700;
    border-bottom: 2px solid #E50914;
}
QTabBar::tab:hover:!selected {
    color: #CCCCCC;
    background-color: rgba(255, 255, 255, 0.04);
    border-bottom: 2px solid rgba(229, 9, 20, 0.25);
}

/* ── Onay Kutusu ────────────────────────────────────────────────── */
QCheckBox {
    color: #D5D5D5;
    spacing: 9px;
    font-size: 13px;
}
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border: 2px solid rgba(255, 255, 255, 0.25);
    border-radius: 4px;
    background-color: rgba(255, 255, 255, 0.04);
}
QCheckBox::indicator:hover {
    border-color: rgba(255, 255, 255, 0.45);
}
QCheckBox::indicator:checked {
    background-color: #E50914;
    border-color: #E50914;
}
QCheckBox:disabled { color: #444444; }
QCheckBox::indicator:disabled {
    border-color: rgba(255, 255, 255, 0.10);
    background-color: transparent;
}

/* ── Mesaj Kutusu ───────────────────────────────────────────────── */
QMessageBox {
    background-color: #191919;
}
QMessageBox QLabel {
    color: #E0E0E0;
    font-size: 13px;
    min-width: 280px;
    line-height: 1.5;
}
QMessageBox QPushButton {
    min-width: 90px;
    min-height: 36px;
}

/* ── Grup Kutusu ────────────────────────────────────────────────── */
QGroupBox {
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 10px;
    margin-top: 22px;
    padding: 12px 12px 12px 12px;
    color: #707070;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.5px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    top: 2px;
    padding: 2px 10px;
    color: #E50914;
    font-size: 13px;
    font-weight: 700;
    background-color: #111111;
}

/* ── Ilerleme Cubugu ─────────────────────────────────────────────── */
QProgressBar {
    background-color: rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    border: none;
    text-align: center;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #9B0610, stop:0.5 #E50914, stop:1 #FF3525);
    border-radius: 4px;
}

/* ── Ipucu ───────────────────────────────────────────────────────── */
QToolTip {
    background-color: #1E1E1E;
    color: #F0F0F0;
    border: 1px solid rgba(255, 255, 255, 0.14);
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
}

/* ── Bolme ───────────────────────────────────────────────────────── */
QSplitter::handle {
    background-color: rgba(255, 255, 255, 0.06);
}

/* ── Kaydirici ───────────────────────────────────────────────────── */
QSlider::groove:horizontal {
    height: 4px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #E50914;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #FFFFFF;
    border: 2px solid #E50914;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #E50914;
    border-color: #FF3525;
}

/* ── Durum Cubugu ────────────────────────────────────────────────── */
QStatusBar {
    background-color: #0A0A0A;
    color: #555555;
    font-size: 11px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

/* ── Scroll Area ─────────────────────────────────────────────────── */
QScrollArea {
    background-color: transparent;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

"""


def get_arrow_style(assets_dir: str) -> str:
    """Spinbox ok gorsellerini QSS'e URL olarak ekler."""
    import os
    up   = os.path.join(assets_dir, "arrow_up.png").replace("\\", "/")
    down = os.path.join(assets_dir, "arrow_down.png").replace("\\", "/")
    return (
        f"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{"
        f" image: url({up}); width: 9px; height: 6px; }}\n"
        f"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{"
        f" image: url({down}); width: 9px; height: 6px; }}\n"
    )
