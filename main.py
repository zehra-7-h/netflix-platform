import sys
import os

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QPalette, QColor


def _create_arrow_assets() -> str:
    """Spinner ok gorsellerini olusturur, assets dizin yolunu dondurur."""
    from PyQt6.QtGui import QPixmap, QPainter, QPolygonF
    from PyQt6.QtCore import QPointF

    assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "assets")
    os.makedirs(assets, exist_ok=True)

    arrows = {
        "arrow_up.png":   [(1, 6), (5, 1), (9, 6)],
        "arrow_down.png": [(1, 1), (5, 6), (9, 1)],
    }
    for filename, pts in arrows.items():
        path = os.path.join(assets, filename)
        pix = QPixmap(10, 7)
        pix.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = QColor("#CCCCCC")
        painter.setPen(c)
        painter.setBrush(c)
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in pts]))
        painter.end()
        pix.save(path, "PNG")

    return assets


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Netflix Platform")

    app.setStyle("Fusion")
    pal = app.palette()
    pal.setColor(QPalette.ColorRole.ButtonText, QColor("#CCCCCC"))
    app.setPalette(pal)

    try:
        from database.connection import db
        db.get_connection()
    except Exception as e:
        QMessageBox.critical(
            None, "Veritabani Hatasi",
            f"Veritabanina baglanamadi:\n{e}\n\n"
            "MSSQL servisinin calistigindan emin olun."
        )
        sys.exit(1)

    assets_dir = _create_arrow_assets()

    from ui.main_window import MainWindow
    window = MainWindow(assets_dir=assets_dir)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
