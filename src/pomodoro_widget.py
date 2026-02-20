from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar,
    QDialog, QFormLayout, QSpinBox, QDialogButtonBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, Qt, pyqtSignal

class PomodoroWidget(QWidget):
    timer_finished = pyqtSignal(int)  # emits task index
    def __init__(self):
        super().__init__()
        self.total_seconds = 25 * 60
        self.remaining = self.total_seconds
        self.running = False
        self.linked_task_index = None  # Required for win detection from MainWindow

        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        self.time_label = QLabel("25:00")
        self.time_label.setFont(QFont("Segoe UI", 72, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, self.total_seconds)
        self.progress.setValue(self.total_seconds)
        self.progress.setTextVisible(True)
        self.progress.setFormat("%m:%s")
        layout.addWidget(self.progress)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        custom_btn = QPushButton("Set Custom Time")
        custom_btn.setFixedSize(220, 60)
        custom_btn.clicked.connect(self.show_duration_dialog)
        btn_layout.addWidget(custom_btn)

        self.start_pause = QPushButton("Start")
        self.start_pause.setFixedSize(180, 60)
        self.start_pause.clicked.connect(self.toggle)
        btn_layout.addWidget(self.start_pause)

        reset_btn = QPushButton("Reset")
        reset_btn.setFixedSize(180, 60)
        reset_btn.clicked.connect(self.reset)
        btn_layout.addWidget(reset_btn)

        layout.addLayout(btn_layout)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

    def start_with_duration(self, seconds, linked_task_index=None):
        """Public method called from MainWindow when clicking 'Start Timer' on a task"""
        self.linked_task_index = linked_task_index  # Link task for win detection
        self.total_seconds = seconds
        self.remaining = seconds
        self.running = True

        # Update UI
        self._update_time_display()
        self.progress.setRange(0, self.total_seconds)
        self.progress.setValue(self.remaining)
        self.start_pause.setText("Pause")

        # Start countdown
        self.timer.start(1000)

    def show_duration_dialog(self):
        dialog = CustomDurationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            hours = dialog.hours_spin.value()
            minutes = dialog.minutes_spin.value()
            total_seconds = (hours * 3600) + (minutes * 60)

            if total_seconds > 0:
                self.start_with_duration(total_seconds)  # Start without task link

    def _update_time_display(self):
        total_secs = self.remaining
        hours = total_secs // 3600
        mins = (total_secs % 3600) // 60
        secs = total_secs % 60

        if hours > 0:
            self.time_label.setText(f"{hours:02d}:{mins:02d}:{secs:02d}")
        else:
            self.time_label.setText(f"{mins:02d}:{secs:02d}")

    def toggle(self):
        if self.running:
            self.timer.stop()
            self.start_pause.setText("Start")
            self.running = False
        else:
            self.timer.start(1000)
            self.start_pause.setText("Pause")
            self.running = True

    def tick(self):
        if self.remaining > 0:
            self.remaining -= 1
            self._update_time_display()
            self.progress.setValue(self.remaining)
        else:
             self.timer.stop()
             self.running = False
             self.start_pause.setText("Time's up!")
             self.time_label.setText("00:00")

            # ✅ Notify MainWindow if this timer was linked to a task
             if self.linked_task_index is not None:
              self.timer_finished.emit(self.linked_task_index)


    def reset(self):
        self.timer.stop()
        self.remaining = self.total_seconds
        self._update_time_display()
        self.progress.setValue(self.total_seconds)
        self.start_pause.setText("Start")
        self.running = False
        self.linked_task_index = None  # Reset link

class CustomDurationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Custom Pomodoro Duration")
        self.setFixedSize(420, 280)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setStyleSheet("""
            QDialog {
                background-color: #161b22;
                color: #c9d1d9;
            }
            QLabel {
                font-size: 16px;
                color: #c9d1d9;
            }
            QSpinBox {
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px;
                font-size: 18px;
            }
            QPushButton {
                background-color: #238636;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                color: white;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Choose your focus duration")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #58a6ff;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setSpacing(15)

        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(0, 8)
        self.hours_spin.setValue(0)
        self.hours_spin.setSuffix(" hours")
        self.hours_spin.setFixedWidth(180)
        form.addRow("Hours:", self.hours_spin)

        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.minutes_spin.setValue(25)
        self.minutes_spin.setSuffix(" minutes")
        self.minutes_spin.setFixedWidth(180)
        form.addRow("Minutes:", self.minutes_spin)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        btn_box.setStyleSheet("QPushButton { min-width: 120px; }")
        layout.addWidget(btn_box, alignment=Qt.AlignmentFlag.AlignCenter)