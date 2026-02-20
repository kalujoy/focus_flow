# src/analytics_widget.py
# FocusFlow – Analytics Widget (Dark Colors + Smooth Animations)

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QScrollArea, QSizePolicy, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import os


# ================= COLOR PALETTE =================
PIE_COLORS = ["#e5533d", "#1f6feb", "#238636", "#a371f7"]
BAR_COLORS = {
    "Low": "#238636",
    "Medium": "#ff9f1c",
    "High": "#e5533d",
}
LINE_COLOR = "#58a6ff"


class AnalyticsWidget(QWidget):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.setup_ui()

    # ================= ANIMATION =================
    def animate_canvas(self, canvas):
        effect = QGraphicsOpacityEffect(canvas)
        canvas.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity", canvas)
        anim.setDuration(500)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()

        canvas._fade_anim = anim  # prevent GC

    # ================= UI =================
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #0d1117; }")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 120)
        content_layout.setSpacing(60)

        title = QLabel("Productivity Analytics")
        title.setFont(QFont("Segoe UI", 42, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #58a6ff;")
        content_layout.addWidget(title)

        # ========== PIE ==========
        pie_title = QLabel("Completed Tasks by Category")
        pie_title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        pie_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie_title.setStyleSheet("color: #c9d1d9;")
        content_layout.addWidget(pie_title)

        self.pie_canvas = FigureCanvas(Figure(figsize=(11, 11), facecolor="#161b22"))
        self.pie_canvas.setMinimumHeight(600)
        self.pie_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.pie_canvas.setStyleSheet("background:#161b22;border-radius:12px;")
        content_layout.addWidget(self.pie_canvas)

        # ========== BAR ==========
        bar_title = QLabel("Completed Tasks by Priority")
        bar_title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        bar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bar_title.setStyleSheet("color: #c9d1d9;")
        content_layout.addWidget(bar_title)

        self.bar_canvas = FigureCanvas(Figure(figsize=(11, 10), facecolor="#161b22"))
        self.bar_canvas.setMinimumHeight(550)
        self.bar_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.bar_canvas.setStyleSheet("background:#161b22;border-radius:12px;")
        content_layout.addWidget(self.bar_canvas)

        # ========== LINE ==========
        line_title = QLabel("Tasks Completed per Day (Last 30 Days)")
        line_title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        line_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_title.setStyleSheet("color: #c9d1d9;")
        content_layout.addWidget(line_title)

        self.line_canvas = FigureCanvas(Figure(figsize=(14, 10), facecolor="#161b22"))
        self.line_canvas.setMinimumHeight(650)
        self.line_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.line_canvas.setStyleSheet("background:#161b22;border-radius:12px;")
        content_layout.addWidget(self.line_canvas)

        # ========== BUTTONS ==========
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(50)
        btn_layout.setContentsMargins(0, 60, 0, 60)

        refresh_btn = QPushButton("Refresh Charts")
        refresh_btn.setFixedHeight(70)
        refresh_btn.setStyleSheet(
            "background:#238636;color:white;font-size:20px;"
            "border-radius:12px;padding:12px;"
        )
        refresh_btn.clicked.connect(self.update_charts)
        btn_layout.addWidget(refresh_btn)

        export_btn = QPushButton("Download Full Report (CSV)")
        export_btn.setFixedHeight(70)
        export_btn.setStyleSheet(
            "background:#1f6feb;color:white;font-size:20px;"
            "border-radius:12px;padding:12px;"
        )
        export_btn.clicked.connect(self.export_report)
        btn_layout.addWidget(export_btn)

        content_layout.addLayout(btn_layout)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.update_charts()

    # ================= UPDATE CHARTS =================
    def update_charts(self):
        completed = [t for t in self.task_manager.tasks if t["done"]]

        if not completed:
            self._show_no_data_message()
            return

        # ---------- PIE ----------
        categories = {}
        for t in completed:
            categories[t.get("category", "Other")] = categories.get(
                t.get("category", "Other"), 0
            ) + 1

        self.pie_canvas.figure.clear()
        ax = self.pie_canvas.figure.add_subplot(111)
        ax.set_facecolor("#0d1117")
        ax.pie(
            categories.values(),
            labels=categories.keys(),
            autopct="%1.1f%%",
            startangle=90,
            colors=PIE_COLORS[:len(categories)],
            textprops={"color": "white", "fontsize": 16, "weight": "bold"},
        )
        ax.axis("equal")
        self.pie_canvas.draw()
        self.animate_canvas(self.pie_canvas)

        # ---------- BAR ----------
        priorities = {"Low": 0, "Medium": 0, "High": 0}
        for t in completed:
            priorities[t.get("priority", "Medium")] += 1

        self.bar_canvas.figure.clear()
        ax = self.bar_canvas.figure.add_subplot(111)
        ax.set_facecolor("#0d1117")
        bars = ax.bar(
            priorities.keys(),
            priorities.values(),
            color=[BAR_COLORS[k] for k in priorities.keys()],
            width=0.6,
        )

        ax.tick_params(colors="white", labelsize=16)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                int(bar.get_height()),
                ha="center",
                color="white",
                fontsize=18,
                fontweight="bold",
            )

        self.bar_canvas.draw()
        self.animate_canvas(self.bar_canvas)

        # ---------- LINE ----------
        end = datetime.now().date()
        start = end - timedelta(days=30)
        dates = pd.date_range(start, end)

        daily = {}
        for t in completed:
            if t.get("due_date"):
                try:
                    d = datetime.fromisoformat(t["due_date"]).date()
                    if start <= d <= end:
                        daily[d] = daily.get(d, 0) + 1
                except:
                    pass

        counts = [daily.get(d.date(), 0) for d in dates]

        self.line_canvas.figure.clear()
        ax = self.line_canvas.figure.add_subplot(111)
        ax.set_facecolor("#0d1117")
        ax.plot(
            dates,
            counts,
            color=LINE_COLOR,
            linewidth=4,
            marker="o",
            markersize=10,
        )

        ax.tick_params(colors="white", labelsize=14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        self.line_canvas.draw()
        self.animate_canvas(self.line_canvas)

    # ================= NO DATA =================
    def _show_no_data_message(self):
        for canvas in (self.pie_canvas, self.bar_canvas, self.line_canvas):
            canvas.figure.clear()
            ax = canvas.figure.add_subplot(111)
            ax.text(
                0.5,
                0.5,
                "No completed tasks yet.\nMark some tasks done to see analytics!",
                ha="center",
                va="center",
                color="#8b949e",
                fontsize=22,
            )
            ax.axis("off")
            canvas.draw()

    # ================= EXPORT =================
    def export_report(self):
        if not self.task_manager.tasks:
            QMessageBox.warning(self, "No Data", "No tasks to export.")
            return

        filename = f"focusflow_report_{datetime.now():%Y%m%d_%H%M%S}.csv"
        pd.DataFrame(self.task_manager.tasks).to_csv(filename, index=False)

        QMessageBox.information(
            self,
            "Export Successful",
            f"Report saved as:\n{os.path.abspath(filename)}",
        )
