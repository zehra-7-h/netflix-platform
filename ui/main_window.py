from PyQt6.QtWidgets import (QMainWindow, QStackedWidget,
                             QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon
from ui.styles.dark_theme import DARK_THEME, get_arrow_style


class MainWindow(QMainWindow):

    def __init__(self, assets_dir: str = ""):
        super().__init__()
        self.setWindowTitle("Netflix Platform")
        self.setMinimumSize(1140, 720)
        sheet = DARK_THEME + (get_arrow_style(assets_dir) if assets_dir else "")
        self.setStyleSheet(sheet)
        self._fade_anim = None   # animasyon referansi GC'den korur

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self._pages = {}
        self._init_auth_pages()
        self._center_on_screen()

    # ── Baslangic ────────────────────────────────────────────────────────────

    def _init_auth_pages(self):
        from ui.pages.login_page import LoginPage
        from ui.pages.register_page import RegisterPage

        self._login_page    = LoginPage()
        self._register_page = RegisterPage()

        self.stack.addWidget(self._login_page)     # index 0
        self.stack.addWidget(self._register_page)  # index 1

        self._login_page.login_success.connect(self._on_login_success)
        self._login_page.go_register.connect(
            lambda: self._fade_to(self._register_page)
        )
        self._register_page.go_login.connect(
            lambda: self._fade_to(self._login_page)
        )
        self._register_page.register_success.connect(
            lambda: self._fade_to(self._login_page)
        )

        self.stack.setCurrentIndex(0)

    def _center_on_screen(self):
        screen = self.screen().availableGeometry()
        w, h = self.minimumWidth(), self.minimumHeight()
        self.setGeometry(
            (screen.width()  - w) // 2,
            (screen.height() - h) // 2,
            w, h
        )

    # ── Gecis animasyonu ──────────────────────────────────────────────────────

    def _fade_to(self, widget):
        """Hedef widget'i fade-in ile goster."""
        effect = widget.graphicsEffect()
        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        effect.setOpacity(0.15)
        self.stack.setCurrentWidget(widget)

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(220)
        anim.setStartValue(0.15)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._fade_anim = anim   # GC'den koru

    # ── Giris / Cikis ────────────────────────────────────────────────────────

    def _on_login_success(self, user):
        if user.is_admin:
            self._load_admin_panel()
        else:
            self._load_user_panel()

    def _load_user_panel(self):
        from ui.pages.user_home_page import UserHomePage
        if "user_home" not in self._pages:
            page = UserHomePage()
            page.logout_requested.connect(self._on_logout)
            self._pages["user_home"] = page
            self.stack.addWidget(page)
        page = self._pages["user_home"]
        page.refresh()
        self._fade_to(page)

    def _load_admin_panel(self):
        from ui.pages.admin.admin_dashboard import AdminDashboard
        if "admin" not in self._pages:
            page = AdminDashboard()
            page.logout_requested.connect(self._on_logout)
            self._pages["admin"] = page
            self.stack.addWidget(page)
        page = self._pages["admin"]
        page.refresh()
        self._fade_to(page)

    def _on_logout(self):
        from services.auth_service import AuthService
        AuthService().logout()
        for key in ["user_home", "admin"]:
            if key in self._pages:
                self.stack.removeWidget(self._pages[key])
                self._pages[key].deleteLater()
                del self._pages[key]
        self._login_page.reset()
        self._fade_to(self._login_page)
