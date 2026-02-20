# # src/pomodoro_widget.py
# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
# from PyQt6.QtCore import QTimer, Qt
# from PyQt6.QtGui import QFont
# import pyqtgraph as pg
# from pyqtgraph import PlotWidget
# import math

# class PomodoroWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.total_seconds = 25 * 60  # Default
#         self.remaining = self.total_seconds
#         self.running = False
#         self.linked_task_index = None

#         self.setup_ui()
#         self.setup_timer()
#         self.setup_circular_plot()

#     def setup_ui(self):
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         # Big time display (overlay)
#         self.time_label = QLabel("25:00")
#         self.time_label.setFont(QFont("Segoe UI", 72, QFont.Weight.Bold))
#         self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.time_label.setStyleSheet("color: #58a6ff; background: transparent;")
#         layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)

#         # Circular plot (will be behind time label)
#         self.plot = PlotWidget(background='#161b22')
#         self.plot.setFixedSize(380, 380)
#         self.plot.setAspectLocked(True)
#         self.plot.hideAxis('bottom')
#         self.plot.hideAxis('left')
#         self.plot.setRange(xRange=[-1.3, 1.3], yRange=[-1.3, 1.3])
#         self.plot.setMouseEnabled(False, False)
#         layout.addWidget(self.plot, alignment=Qt.AlignmentFlag.AlignCenter)

#         # Buttons
#         btn_layout = QHBoxLayout()
#         btn_layout.setSpacing(30)

#         self.start_pause_btn = QPushButton("▶ Start")
#         self.start_pause_btn.setFixedSize(180, 60)
#         self.start_pause_btn.clicked.connect(self.toggle)
#         btn_layout.addWidget(self.start_pause_btn)

#         reset_btn = QPushButton("Reset")
#         reset_btn.setFixedSize(180, 60)
#         reset_btn.clicked.connect(self.reset)
#         btn_layout.addWidget(reset_btn)

#         layout.addLayout(btn_layout)

#     def setup_timer(self):
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.tick)

#     def setup_circular_plot(self):
#         """Initialize empty plot - we'll redraw on tick"""
#         self.plot.clear()
#         self._draw_background_circle()
#         self._draw_progress_arc(1.0)  # full at start

#     def start_with_duration(self, seconds, linked_task_index=None):
#         """Start with custom duration (called from task)"""
#         self.total_seconds = seconds
#         self.remaining = seconds
#         self.linked_task_index = linked_task_index
#         mins, secs = divmod(seconds, 60)
#         self.time_label.setText(f"{mins:02d}:{secs:02d}")
#         self._draw_progress_arc(1.0)
#         self.start_pause_btn.setText("Pause")
#         self.running = True
#         self.timer.start(1000)

#     def toggle(self):
#         if self.running:
#             self.timer.stop()
#             self.start_pause_btn.setText("▶ Start")
#             self.running = False
#         else:
#             self.timer.start(1000)
#             self.start_pause_btn.setText("Pause")
#             self.running = True

#     def tick(self):
#         if self.remaining > 0:
#             self.remaining -= 1
#             mins, secs = divmod(self.remaining, 60)
#             self.time_label.setText(f"{mins:02d}:{secs:02d}")

#             # Update progress (0.0 to 1.0)
#             progress = self.remaining / self.total_seconds if self.total_seconds > 0 else 0
#             self._draw_progress_arc(progress)
#         else:
#             self.timer.stop()
#             self.running = False
#             self.start_pause_btn.setText("Done!")
#             self.time_label.setText("00:00")

#     def reset(self):
#         self.timer.stop()
#         self.running = False
#         self.start_pause_btn.setText("▶ Start")
#         self.remaining = self.total_seconds
#         mins, secs = divmod(self.remaining, 60)
#         self.time_label.setText(f"{mins:02d}:{secs:02d}")
#         self._draw_progress_arc(1.0)

#     def _draw_background_circle(self):
#         """Static gray background circle"""
#         circle = pg.QtWidgets.QGraphicsEllipseItem(-1, -1, 2, 2)
#         circle.setPen(pg.mkPen('#30363d', width=20))
#         circle.setBrush(pg.mkBrush(None))
#         self.plot.addItem(circle)

#     def _draw_progress_arc(self, progress):
#         """Redraw the blue progress arc (0.0 to 1.0)"""
#         self.plot.clear()
#         self._draw_background_circle()

#         if progress <= 0:
#             return

#         # Angle in degrees (full = 360, starts at top)
#         angle = 360 * progress

#         # Create arc
#         arc = pg.QtWidgets.QGraphicsArcItem(-1, -1, 2, 2)
#         arc.setStartAngle(90 * 16)  # Start at top (Qt uses 1/16th degrees)
#         arc.setSpanAngle(-angle * 16)  # Negative = clockwise
#         arc.setPen(pg.mkPen('#58a6ff', width=20))
#         self.plot.addItem(arc)