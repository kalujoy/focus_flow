# import sys
# import json
# import os
# from pathlib import Path
# from datetime import datetime
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QPushButton, QTabWidget, QFrame, QListWidget, QLineEdit, QComboBox,
#     QCheckBox, QListWidgetItem
# )
# from PyQt6.QtCore import Qt, QTimer, QTime
# from PyQt6.QtGui import QFont, QColor

# DATA_FILE = "data/tasks.json"

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("FocusFlow - To-Do + Pomodoro + Analytics")
#         self.setGeometry(100, 100, 1200, 850)

#         # Data
#         self.tasks = self.load_tasks()  # list of dicts: {"text": str, "priority": str, "done": bool, "created": str}

#         # Central widget
#         central = QWidget()
#         self.setCentralWidget(central)
#         main_layout = QVBoxLayout(central)
#         main_layout.setContentsMargins(30, 30, 30, 30)
#         main_layout.setSpacing(20)

#         # Header
#         header = QLabel("FocusFlow")
#         header.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
#         header.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         header.setStyleSheet("color: #bb86fc;")
#         main_layout.addWidget(header)

#         # Tabs
#         self.tabs = QTabWidget()
#         self.tabs.setDocumentMode(True)
#         self.tabs.setTabPosition(QTabWidget.TabPosition.North)
#         self.apply_tab_styles()
#         main_layout.addWidget(self.tabs)

#         self.setup_tasks_tab()
#         self.setup_pomodoro_tab()
#         self.setup_analytics_tab()

#     def apply_tab_styles(self):
#         self.tabs.setStyleSheet("""
#             QTabWidget::pane {
#                 border: 1px solid #30363d;
#                 background: #161b22;
#                 border-radius: 8px;
#             }
#             QTabBar::tab {
#                 background: #0d1117;
#                 color: #8b949e;
#                 padding: 14px 28px;
#                 margin-right: 4px;
#                 font-size: 15px;
#                 border-top-left-radius: 8px;
#                 border-top-right-radius: 8px;
#             }
#             QTabBar::tab:selected {
#                 background: #21262d;
#                 color: white;
#                 border-bottom: 3px solid #bb86fc;
#             }
#             QTabBar::tab:hover:!selected {
#                 background: #1f2937;
#             }
#         """)

#     # ── TASKS TAB ───────────────────────────────────────────────────────────────
#     def setup_tasks_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout(tab)
#         layout.setSpacing(16)

#         # Input + Priority + Add
#         input_row = QHBoxLayout()
#         input_row.setSpacing(12)

#         self.task_input = QLineEdit()
#         self.task_input.setPlaceholderText("What needs to be done?")
#         self.task_input.setMinimumHeight(48)
#         self.task_input.returnPressed.connect(self.add_task)
#         input_row.addWidget(self.task_input)

#         self.priority_combo = QComboBox()
#         self.priority_combo.addItems(["Low", "Medium", "High"])
#         self.priority_combo.setFixedWidth(140)
#         input_row.addWidget(self.priority_combo)

#         add_btn = QPushButton("Add Task")
#         add_btn.setFixedSize(140, 48)
#         add_btn.clicked.connect(self.add_task)
#         input_row.addWidget(add_btn)

#         layout.addLayout(input_row)

#         # Task list
#         self.task_list = QListWidget()
#         self.task_list.setStyleSheet("""
#             QListWidget {
#                 background: #0d1117;
#                 border: none;
#                 border-radius: 8px;
#             }
#             QListWidget::item {
#                 padding: 12px 16px;
#                 border-bottom: 1px solid #21262d;
#                 color: #c9d1d9;
#             }
#             QListWidget::item:selected {
#                 background: #21262d;
#             }
#         """)
#         layout.addWidget(self.task_list)

#         self.refresh_task_list()

#         self.tabs.addTab(tab, "📝 Tasks")

#     def load_tasks(self):
#         if os.path.exists(DATA_FILE):
#             try:
#                 with open(DATA_FILE, 'r', encoding='utf-8') as f:
#                     return json.load(f)
#             except:
#                 return []
#         return []

#     def save_tasks(self):
#         os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
#         with open(DATA_FILE, 'w', encoding='utf-8') as f:
#             json.dump(self.tasks, f, indent=2)

#     def add_task(self):
#         text = self.task_input.text().strip()
#         if not text:
#             return

#         priority = self.priority_combo.currentText()
#         task = {
#             "text": text,
#             "priority": priority,
#             "done": False,
#             "created": datetime.now().isoformat()
#         }
#         self.tasks.append(task)
#         self.save_tasks()
#         self.refresh_task_list()
#         self.task_input.clear()

#     def refresh_task_list(self):
#         self.task_list.clear()
#         for task in self.tasks:
#             item = QListWidgetItem()
#             prefix = "✓ " if task["done"] else "  "
#             text = f"{prefix}{task['text']}"
#             item.setText(text)

#             # Priority color badge
#             color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}.get(task["priority"], "#6b7280")
#             item.setForeground(QColor(color))

#             # Strikethrough for done
#             if task["done"]:
#                 font = item.font()
#                 font.setStrikeOut(True)
#                 item.setFont(font)

#             self.task_list.addItem(item)

#     # ── POMODORO TAB ────────────────────────────────────────────────────────────
#     def setup_pomodoro_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout(tab)
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.setSpacing(30)

#         self.timer_display = QLabel("25:00")
#         self.timer_display.setFont(QFont("Segoe UI", 72, QFont.Weight.Bold))
#         self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.timer_display)

#         btn_layout = QHBoxLayout()
#         btn_layout.setSpacing(20)

#         self.start_pause_btn = QPushButton("Start")
#         self.start_pause_btn.setFixedSize(180, 70)
#         self.start_pause_btn.clicked.connect(self.toggle_pomodoro)
#         btn_layout.addWidget(self.start_pause_btn)

#         reset_btn = QPushButton("Reset")
#         reset_btn.setFixedSize(180, 70)
#         reset_btn.clicked.connect(self.reset_pomodoro)
#         btn_layout.addWidget(reset_btn)

#         layout.addLayout(btn_layout)

#         self.pomo_timer = QTimer(self)
#         self.pomo_timer.timeout.connect(self.update_pomodoro)
#         self.remaining_time = 25 * 60
#         self.is_running = False

#         self.tabs.addTab(tab, "⏳ Pomodoro")

#     def toggle_pomodoro(self):
#         if self.is_running:
#             self.pomo_timer.stop()
#             self.start_pause_btn.setText("Start")
#             self.is_running = False
#         else:
#             self.pomo_timer.start(1000)
#             self.start_pause_btn.setText("Pause")
#             self.is_running = True

#     def update_pomodoro(self):
#         if self.remaining_time > 0:
#             self.remaining_time -= 1
#             mins = self.remaining_time // 60
#             secs = self.remaining_time % 60
#             self.timer_display.setText(f"{mins:02d}:{secs:02d}")
#         else:
#             self.pomo_timer.stop()
#             self.start_pause_btn.setText("Start")
#             self.is_running = False
#             self.timer_display.setText("Time's up!")

#     def reset_pomodoro(self):
#         self.pomo_timer.stop()
#         self.remaining_time = 25 * 60
#         self.timer_display.setText("25:00")
#         self.start_pause_btn.setText("Start")
#         self.is_running = False

#     # ── ANALYTICS TAB (placeholder) ─────────────────────────────────────────────
#     def setup_analytics_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout(tab)
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         label = QLabel("Productivity Analytics\n(Coming soon: charts with matplotlib)")
#         label.setFont(QFont("Segoe UI", 24))
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         self.tabs.addTab(tab, "📊 Analytics")

# def main():
#     app = QApplication(sys.argv)
#     app.setStyle('Fusion')

#     # Load external stylesheet
#     try:
#         with open("styles.qss", "r", encoding="utf-8") as f:
#             app.setStyleSheet(f.read())
#     except FileNotFoundError:
#         print("Warning: styles.qss not found. Using default style.")

#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
# # def main():
# #     app = QApplication(sys.argv)
# #     app.setStyle('Fusion')

# #     # Enhanced dark theme
# #     app.setStyleSheet("""
# #         QMainWindow {
# #             background-color: #0d1117;
# #         }
# #         QLabel {
# #             color: #c9d1d9;
# #         }
# #         QLineEdit, QComboBox {
# #             background-color: #161b22;
# #             border: 1px solid #30363d;
# #             border-radius: 8px;
# #             padding: 10px;
# #             color: #c9d1d9;
# #             font-size: 15px;
# #         }
# #         QPushButton {
# #             background-color: #238636;
# #             border: none;
# #             border-radius: 8px;
# #             padding: 12px 24px;
# #             color: white;
# #             font-size: 15px;
# #             font-weight: 500;
# #         }
# #         QPushButton:hover {
# #             background-color: #2ea043;
# #         }
# #         QPushButton:pressed {
# #             background-color: #1a7f37;
# #         }
# #     """)

# #     window = MainWindow()
# #     window.show()
# #     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()




# main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Load beautiful dark theme
    try:
        with open("styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found - using default style.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())