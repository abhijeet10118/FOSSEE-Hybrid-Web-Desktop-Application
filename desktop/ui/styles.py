BG_DARK = "#0d1117"
SURFACE = "#161b22"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#58a6ff"
ACCENT_HOVER = "#79b8ff"
SUCCESS = "#3fb950"
DANGER = "#f85149"
CARD_BG = "#21262d"

MAIN_STYLESHEET = f"""
    QMainWindow, QDialog, QWidget {{
        background-color: {BG_DARK};
    }}
    QLabel {{
        color: {TEXT};
        font-size: 13px;
    }}
    QPushButton {{
        background-color: {SURFACE};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {BORDER};
        border-color: {MUTED};
    }}
    QPushButton:pressed {{
        background-color: {CARD_BG};
    }}
    QPushButton:disabled {{
        color: {MUTED};
        background-color: {SURFACE};
    }}
    QPushButton#primaryBtn {{
        background-color: {ACCENT};
        color: white;
        border: none;
    }}
    QPushButton#primaryBtn:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QLineEdit {{
        background-color: {BG_DARK};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 13px;
        selection-background-color: {ACCENT};
    }}
    QLineEdit:focus {{
        border-color: {ACCENT};
    }}
    QLineEdit::placeholder {{
        color: {MUTED};
    }}
    QGroupBox {{
        color: {TEXT};
        font-size: 13px;
        font-weight: 600;
        border: 1px solid {BORDER};
        border-radius: 8px;
        margin-top: 12px;
        padding: 16px;
        padding-top: 24px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 0 8px;
        background-color: {BG_DARK};
        color: {MUTED};
    }}
    QListWidget {{
        background-color: {SURFACE};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 4px;
        font-size: 13px;
    }}
    QListWidget::item {{
        padding: 10px 12px;
        border-radius: 4px;
    }}
    QListWidget::item:selected {{
        background-color: rgba(88, 166, 255, 0.2);
        color: {ACCENT};
    }}
    QListWidget::item:hover {{
        background-color: {CARD_BG};
    }}
    QTabWidget::pane {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        margin-top: -1px;
        padding: 16px;
    }}
    QTabBar::tab {{
        background-color: {SURFACE};
        color: {MUTED};
        border: 1px solid {BORDER};
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 10px 20px;
        margin-right: 2px;
        font-size: 13px;
    }}
    QTabBar::tab:selected {{
        background-color: {SURFACE};
        color: {ACCENT};
        font-weight: 600;
        border-color: {BORDER};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {CARD_BG};
    }}
    QTableWidget {{
        background-color: {SURFACE};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 8px;
        gridline-color: {BORDER};
        font-size: 13px;
    }}
    QTableWidget::item {{
        padding: 8px;
    }}
    QHeaderView::section {{
        background-color: {CARD_BG};
        color: {MUTED};
        padding: 10px;
        border: none;
        border-bottom: 2px solid {BORDER};
        font-weight: 600;
    }}
    QScrollBar:vertical {{
        background: {SURFACE};
        width: 10px;
        border-radius: 5px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {BORDER};
        border-radius: 5px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {MUTED};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QFrame#header {{
        padding: 4px 0;
        border-bottom: 1px solid {BORDER};
    }}
"""

LOGIN_STYLESHEET = f"""
    QDialog {{
        background-color: {BG_DARK};
    }}
    QLabel#title {{
        color: {TEXT};
        font-size: 20px;
        font-weight: 700;
    }}
    QLabel#subtitle {{
        color: {MUTED};
        font-size: 13px;
    }}
    QLabel#error {{
        color: {DANGER};
        font-size: 12px;
    }}
"""

MPL_STYLE = {
    "figure.facecolor": BG_DARK,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": BORDER,
    "axes.labelcolor": TEXT,
    "text.color": TEXT,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "grid.color": BORDER,
}
