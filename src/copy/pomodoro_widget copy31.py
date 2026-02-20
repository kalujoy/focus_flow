from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class PomodoroWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        self.time_label = QLabel("25:00")
        self.time_label.setFont(QFont("Segoe UI", 72, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 25*60)
        self.progress.setValue(25*60)
        self.progress.setTextVisible(True)
        self.progress.setFormat("%m:%s")
        layout.addWidget(self.progress)

        btn_layout = QHBoxLayout()
        self.start_pause = QPushButton("Start")
        self.start_pause.setFixedSize(180, 60)
        self.start_pause.clicked.connect(self.toggle)
        btn_layout.addWidget(self.start_pause)

        reset_btn = QPushButton("Reset")
        reset_btn.setFixedSize(180, 60)
        reset_btn.clicked.connect(self.reset)
        btn_layout.addWidget(reset_btn)

        layout.addLayout(btn_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.total_seconds = 25 * 60
        self.remaining = self.total_seconds
        self.running = False
        self.linked_task_index = None

    def start_with_duration(self, seconds, linked_task_index=None):
        self.total_seconds = seconds
        self.remaining = seconds
        self.linked_task_index = linked_task_index
        mins, secs = divmod(seconds, 60)
        self.time_label.setText(f"{mins:02d}:{secs:02d}")
        self.progress.setRange(0, seconds)
        self.progress.setValue(seconds)
        self.start_pause.setText("Pause")
        self.running = True
        self.timer.start(1000)

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
            mins, secs = divmod(self.remaining, 60)
            self.time_label.setText(f"{mins:02d}:{secs:02d}")
            self.progress.setValue(self.remaining)
        else:
            self.timer.stop()
            self.running = False
            self.start_pause.setText("Time's up!")
            self.time_label.setText("00:00")

    def reset(self):
        self.timer.stop()
        self.remaining = self.total_seconds
        self.time_label.setText(f"{self.total_seconds//60:02d}:00")
        self.progress.setValue(self.total_seconds)
        self.start_pause.setText("Start")
        self.running = False
        self.linked_task_index = None