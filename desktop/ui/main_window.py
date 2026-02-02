from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QListWidget,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QScrollArea,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("Qt5Agg")

from api_client import ApiClient


class MainWindow(QMainWindow):
    def __init__(self, client: ApiClient):
        super().__init__()
        self.client = client
        self.current_dataset = None
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setMinimumSize(900, 650)
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        top = QHBoxLayout()
        top.addWidget(QLabel("Chemical Equipment Parameter Visualizer"))
        top.addStretch()
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        top.addWidget(self.upload_btn)
        logout_btn = QPushButton("Log out")
        logout_btn.clicked.connect(self.close)
        top.addWidget(logout_btn)
        layout.addLayout(top)

        history_box = QGroupBox("Last 5 uploads")
        history_layout = QVBoxLayout(history_box)
        self.history_list = QListWidget()
        self.history_list.itemSelectionChanged.connect(self.on_history_selected)
        history_layout.addWidget(self.history_list)
        self.pdf_btn = QPushButton("Download PDF report")
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setEnabled(False)
        history_layout.addWidget(self.pdf_btn)
        layout.addWidget(history_box)

        self.tabs = QTabWidget()
        summary_w = QWidget()
        summary_layout = QVBoxLayout(summary_w)
        self.summary_label = QLabel("Upload a CSV or select a dataset from history.")
        self.summary_label.setWordWrap(True)
        summary_layout.addWidget(self.summary_label)
        summary_btn_row = QHBoxLayout()
        self.download_summary_btn = QPushButton("Download Summary")
        self.download_summary_btn.clicked.connect(self.download_summary)
        self.download_summary_btn.setEnabled(False)
        summary_btn_row.addWidget(self.download_summary_btn)
        summary_btn_row.addStretch()
        summary_layout.addLayout(summary_btn_row)
        self.tabs.addTab(summary_w, "Summary")

        charts_w = QWidget()
        charts_scroll = QScrollArea()
        charts_scroll.setWidgetResizable(True)
        charts_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        charts_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        charts_inner = QWidget()
        charts_layout = QVBoxLayout(charts_inner)
        self.chart_canvas_type = None
        self.chart_canvas_avg = None
        charts_layout.addWidget(QLabel("Type distribution"))
        self.chart_container_type = QWidget()
        self.chart_container_type.setMinimumHeight(320)
        self.chart_container_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.chart_layout_type = QVBoxLayout(self.chart_container_type)
        self.chart_layout_type.setContentsMargins(0, 0, 0, 0)
        self.chart_placeholder_type = QLabel("(No data)")
        self.chart_layout_type.addWidget(self.chart_placeholder_type)
        charts_layout.addWidget(self.chart_container_type)
        charts_layout.addWidget(QLabel("Parameter averages"))
        self.chart_container_avg = QWidget()
        self.chart_container_avg.setMinimumHeight(320)
        self.chart_container_avg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.chart_layout_avg = QVBoxLayout(self.chart_container_avg)
        self.chart_layout_avg.setContentsMargins(0, 0, 0, 0)
        self.chart_placeholder_avg = QLabel("(No data)")
        self.chart_layout_avg.addWidget(self.chart_placeholder_avg)
        charts_layout.addWidget(self.chart_container_avg)
        charts_scroll.setWidget(charts_inner)
        charts_main_layout = QVBoxLayout(charts_w)
        charts_main_layout.setContentsMargins(0, 0, 0, 0)
        charts_main_layout.addWidget(charts_scroll)
        self.tabs.addTab(charts_w, "Charts")

        table_w = QWidget()
        table_layout = QVBoxLayout(table_w)
        self.table = QTableWidget()
        table_layout.addWidget(self.table)
        self.tabs.addTab(table_w, "Data table")

        layout.addWidget(self.tabs)

        self.refresh_history()

    def refresh_history(self):
        try:
            history = self.client.get_history()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            return
        self.history_list.clear()
        self.history_items = history
        for item in history:
            name = item.get("name", "?")
            count = item.get("row_count", 0)
            self.history_list.addItem(f"{name} — {count} rows (id: {item.get('id')})")

    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV (*.csv)"
        )
        if not path:
            return
        try:
            data = self.client.upload_csv(path)
            self.current_dataset = data
            self.refresh_history()
            self.render_current()
            QMessageBox.information(self, "Upload", "File uploaded successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Upload failed", str(e))

    def on_history_selected(self):
        row = self.history_list.currentRow()
        if row < 0 or row >= len(self.history_items):
            self.pdf_btn.setEnabled(False)
            self.download_summary_btn.setEnabled(False)
            return
        self.pdf_btn.setEnabled(True)
        self.download_summary_btn.setEnabled(True)
        item = self.history_items[row]
        try:
            self.current_dataset = self.client.get_dataset(item["id"])
            self.render_current()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def download_pdf(self):
        row = self.history_list.currentRow()
        if row < 0 or row >= len(self.history_items):
            return
        item = self.history_items[row]
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", f"report_{item.get('name', 'dataset')}.pdf", "PDF (*.pdf)"
        )
        if not path:
            return
        try:
            self.client.download_pdf(item["id"], path)
            QMessageBox.information(self, "PDF", f"Saved to {path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def download_summary(self):
        if not self.current_dataset:
            return
        summary = self.current_dataset.get("summary") or {}
        name = self.current_dataset.get("name", "dataset")
        safe_name = name.replace(".csv", "").replace(" ", "_")[:50]
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Summary", f"summary_{safe_name}.json", "JSON (*.json)"
        )
        if not path:
            return
        try:
            data = {"name": name, **summary}
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            QMessageBox.information(self, "Summary", f"Saved to {path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def render_current(self):
        if not self.current_dataset:
            self.summary_label.setText("Upload a CSV or select a dataset from history.")
            self.download_summary_btn.setEnabled(False)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.clear_charts()
            return
        self.download_summary_btn.setEnabled(True)
        summary = self.current_dataset.get("summary") or {}
        raw_data = self.current_dataset.get("raw_data") or []
        name = self.current_dataset.get("name", "Dataset")

        total = summary.get("total_count", 0)
        av = summary.get("averages", {})
        td = summary.get("type_distribution", {})
        lines = [f"Dataset: {name}", f"Total equipment: {total}"]
        if av:
            lines.append("Averages: " + ", ".join(f"{k}={v}" for k, v in av.items()))
        if td:
            lines.append("By type: " + ", ".join(f"{k}: {v}" for k, v in td.items()))
        self.summary_label.setText("\n".join(lines))

        if raw_data:
            cols = list(raw_data[0].keys())
            self.table.setColumnCount(len(cols))
            self.table.setHorizontalHeaderLabels(cols)
            self.table.setRowCount(len(raw_data))
            for i, row in enumerate(raw_data):
                for j, c in enumerate(cols):
                    self.table.setItem(i, j, QTableWidgetItem(str(row.get(c, ""))))
        else:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)

        self.draw_charts(summary)

    def clear_charts(self):
        while self.chart_layout_type.count():
            item = self.chart_layout_type.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()
        self.chart_placeholder_type = QLabel("(No data)")
        self.chart_layout_type.addWidget(self.chart_placeholder_type)

        while self.chart_layout_avg.count():
            item = self.chart_layout_avg.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()
        self.chart_placeholder_avg = QLabel("(No data)")
        self.chart_layout_avg.addWidget(self.chart_placeholder_avg)

        self.chart_canvas_type = None
        self.chart_canvas_avg = None

    def draw_charts(self, summary):
        self.clear_charts()
        td = summary.get("type_distribution") or {}
        av = summary.get("averages") or {}

        if td:
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(
                list(td.values()),
                labels=list(td.keys()),
                autopct="%1.0f%%",
                startangle=90,
            )
            ax.set_title("Equipment type distribution")
            fig.tight_layout(pad=1.2)
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(300)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.chart_layout_type.removeWidget(self.chart_placeholder_type)
            self.chart_placeholder_type.setParent(None)
            self.chart_placeholder_type.deleteLater()
            self.chart_layout_type.addWidget(canvas)
            self.chart_canvas_type = canvas
            canvas.draw()

        if av:
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.bar(list(av.keys()), [float(v) for v in av.values()], color="steelblue")
            ax.set_ylabel("Average value")
            ax.set_title("Parameter averages")
            fig.tight_layout(pad=1.2)
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(300)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.chart_layout_avg.removeWidget(self.chart_placeholder_avg)
            self.chart_placeholder_avg.setParent(None)
            self.chart_placeholder_avg.deleteLater()
            self.chart_layout_avg.addWidget(canvas)
            self.chart_canvas_avg = canvas
            canvas.draw()
