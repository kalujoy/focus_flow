# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
# from PyQt6.QtCore import QTimer, Qt
# from PyQt6.QtGui import QFont
# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
# )
# from PyQt6.QtCore import QTimer, Qt
# from PyQt6.QtGui import QFont

# class PomodoroWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.setSpacing(30)

#         self.time_label = QLabel("25:00")
#         self.time_label.setFont(QFont("Segoe UI", 72, QFont.Weight.Bold))
#         self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.time_label)

#         self.progress = QProgressBar()
#         self.progress.setRange(0, 25*60)
#         self.progress.setValue(25*60)
#         self.progress.setTextVisible(True)
#         self.progress.setFormat("%m:%s")
#         layout.addWidget(self.progress)

#         btn_layout = QHBoxLayout()
#         self.start_pause = QPushButton("Start")
#         self.start_pause.setFixedSize(180, 60)
#         self.start_pause.clicked.connect(self.toggle)
#         btn_layout.addWidget(self.start_pause)

#         reset_btn = QPushButton("Reset")
#         reset_btn.setFixedSize(180, 60)
#         reset_btn.clicked.connect(self.reset)
#         btn_layout.addWidget(reset_btn)

#         layout.addLayout(btn_layout)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.tick)
#         self.remaining = 25 * 60
#         self.running = False

#     def toggle(self):
#         if self.running:
#             self.timer.stop()
#             self.start_pause.setText("Start")
#             self.running = False
#         else:
#             self.timer.start(1000)
#             self.start_pause.setText("Pause")
#             self.running = True

#     def tick(self):
#         if self.remaining > 0:
#             self.remaining -= 1
#             mins, secs = divmod(self.remaining, 60)
#             self.time_label.setText(f"{mins:02d}:{secs:02d}")
#             self.progress.setValue(self.remaining)
#         else:
#             self.timer.stop()
#             self.running = False
#             self.start_pause.setText("Start")
#             self.time_label.setText("Time's up!")

#     def reset(self):
#         self.timer.stop()
#         self.remaining = 25 * 60
#         self.time_label.setText("25:00")
#         self.progress.setValue(self.remaining)
#         self.start_pause.setText("Start")
#         self.running = False
#         def start_with_duration(self, seconds, linked_task_index=None):
#     """Start timer with custom duration and link to specific task"""
#     self.total_seconds = seconds
#     self.remaining = seconds
#     self.linked_task_index = linked_task_index  # For win detection later
#     mins, secs = divmod(seconds, 60)
#     self.time_label.setText(f"{mins:02d}:{secs:02d}")
#     # Update your progress bar/circle here
#     self.start_pause.setText("Pause")
#     self.running = True
#     self.timer.start(1000)


# src/pomodoro_widget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPen, QColor
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import math

class PomodoroWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_state()
        self.setup_circular_timer()

    def setup_ui(self):
        """Setup the main layout and basic UI elements"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Main timer display (will be overlaid on circular timer)
        self.time_label = QLabel("25:00")
        self.time_label.setFont(QFont("Segoe UI", 64, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("color: #58a6ff; background: transparent;")
        layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Circular timer plot (will be added below)
        layout.addWidget(self.circular_plot, alignment=Qt.AlignmentFlag.AlignCenter)

        # Control buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.start_pause = QPushButton("▶️ Start")
        self.start_pause.setFixedSize(200, 60)
        self.start_pause.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.start_pause.clicked.connect(self.toggle_timer)
        btn_layout.addWidget(self.start_pause)

        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.setFixedSize(200, 60)
        self.reset_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.reset_btn.clicked.connect(self.reset)
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

        # Status label (shows linked task or general status)
        self.status_label = QLabel("Ready to focus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #8b949e; font-size: 14px;")
        layout.addWidget(self.status_label)

    def setup_state(self):
        """Initialize timer state variables"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        # Timer state
        self.total_seconds = 25 * 60  # Default 25 minutes
        self.remaining = self.total_seconds
        self.running = False
        
        # Task linking for win detection
        self.linked_task_index = None
        self.start_time = None

    def setup_circular_timer(self):
        """Create beautiful circular animated timer using pyqtgraph"""
        # Create plot widget for circular timer
        self.circular_plot = PlotWidget(background='#161b22')
        self.circular_plot.setFixedSize(300, 300)
        self.circular_plot.setAspectLocked(True)
        self.circular_plot.hideAxis('bottom')
        self.circular_plot.hideAxis('left')
        self.circular_plot.setRange(xRange=[-1.2, 1.2], yRange=[-1.2, 1.2], padding=0)
        self.circular_plot.setMouseEnabled(False, False)
        self.circular_plot.showGrid(x=False, y=False)
        
        # Set dark theme colors
        self.circular_plot.setBackground('#161b22')
        pg.setConfigOption('background', '#161b22')
        pg.setConfigOption('foreground', '#58a6ff')

        # Initialize with full circle
        self._draw_circular_progress(1.0)  # 100% full

    def start_with_duration(self, seconds, linked_task_index=None):
        """
        Start timer with custom duration and link to specific task
        
        Args:
            seconds (int): Total timer duration in seconds
            linked_task_index (int, optional): Index of linked task for win detection
        """
        self.total_seconds = seconds
        self.remaining = seconds
        self.linked_task_index = linked_task_index
        
        # Record start time for win calculations
        self.start_time = self.timer.elapsed() if self.start_time else 0
        
        # Update display
        mins, secs = divmod(seconds, 60)
        self.time_label.setText(f"{mins:02d}:{secs:02d}")
        
        # Update circular progress (full circle to start)
        self._draw_circular_progress(1.0)
        
        # Update status
        if linked_task_index is not None:
            task_name = self.parent().task_manager.tasks[linked_task_index]["text"][:20] + "..."
            self.status_label.setText(f"🔗 Linked to: {task_name}")
            self.status_label.setStyleSheet("color: #58a6ff; font-size: 14px;")
        else:
            self.status_label.setText("⏱️ Custom session")
            self.status_label.setStyleSheet("color: #8b949e; font-size: 14px;")
        
        # Start timer
        self.start_pause.setText("⏸️ Pause")
        self.running = True
        self.timer.start(1000)  # 1 second intervals

    def toggle_timer(self):
        """Toggle between start/pause states"""
        if self.running:
            self.timer.stop()
            self.start_pause.setText("▶️ Start")
            self.running = False
        else:
            self.timer.start(1000)
            self.start_pause.setText("⏸️ Pause")
            self.running = True

    def tick(self):
        """Timer tick - update every second"""
        if self.remaining > 0:
            self.remaining -= 1
            
            # Update time display
            mins, secs = divmod(self.remaining, 60)
            self.time_label.setText(f"{mins:02d}:{secs:02d}")
            
            # Update circular progress
            progress = self.remaining / self.total_seconds if self.total_seconds > 0 else 0
            self._draw_circular_progress(progress)
            
            # Change color based on time remaining (optional visual cue)
            if progress < 0.2:  # Last 20%
                self.time_label.setStyleSheet("color: #ff5252; background: transparent;")  # Red
            elif progress < 0.5:  # Last 50%
                self.time_label.setStyleSheet("color: #ffb300; background: transparent;")  # Orange
            else:
                self.time_label.setStyleSheet("color: #58a6ff; background: transparent;")  # Blue
                
        else:
            # Timer finished
            self.timer_finished()

    def timer_finished(self):
        """Handle timer completion"""
        self.running = False
        self.start_pause.setText("🎉 Session Complete!")
        self.time_label.setText("00:00")
        self.time_label.setStyleSheet("color: #4caf50; background: transparent;")
        
        # Check for win condition if linked to a task
        if self.linked_task_index is not None:
            time_remaining = self.remaining
            if time_remaining > 0:  # Finished early (win!)
                self._trigger_win()
            else:
                self.status_label.setText("⏰ Time's up - great effort!")
        
        # Reset after 3 seconds
        QTimer.singleShot(3000, self.reset)

    def _trigger_win(self):
        """Handle win condition - task completed before time ended"""
        # Emit signal or call parent method to mark win
        # For now, just show celebration
        self.status_label.setText("🏆 WIN! Early completion!")
        self.status_label.setStyleSheet("color: #4caf50; font-size: 16px; font-weight: bold;")
        
        # Optional: Play sound, show confetti, etc.
        # You can add more celebration effects here

    def _draw_circular_progress(self, progress):
        """Draw animated circular progress indicator"""
        # Clear previous items
        self.circular_plot.clear()
        
        # Calculate angle for arc (0-360 degrees, starting from top)
        if progress == 1.0:
            angle = 360
        else:
            angle = 360 * progress
        
        # Center point and radius
        center_x, center_y = 0, 0
        radius = 0.8
        
        # Background circle (gray outline)
        bg_circle = pg.CircleROI(
            pos=(center_x - radius, center_y - radius),
            size=(radius * 2, radius * 2),
            parent=self.circular_plot.plotItem,
            pen=pg.mkPen(color='#30363d', width=8),
            movable=False,
            removable=False
        )
        self.circular_plot.addItem(bg_circle)
        
        # Progress arc (blue, animated)
        if progress > 0:
            # Create arc points
            num_points = 100
            arc_points = []
            
            for i in range(num_points):
                t = (i / num_points) * angle
                # Start from top (90 degrees) and go clockwise
                x = center_x + radius * math.cos(math.radians(90 - t))
                y = center_y + radius * math.sin(math.radians(90 - t))
                arc_points.append((x, y))
            
            # Create curve from points
            arc_curve = pg.PlotDataItem(
                arc_points,
                pen=pg.mkPen(color='#58a6ff', width=8),
                connect='finite'
            )
            self.circular_plot.addItem(arc_curve)
        
        # Center dot (current progress indicator)
        center_dot = pg.CircleROI(
            pos=(center_x - 0.05, center_y - 0.05),
            size=(0.1, 0.1),
            parent=self.circular_plot.plotItem,
            pen=None,
            brush=pg.mkBrush('#58a6ff'),
            movable=False,
            removable=False
        )
        self.circular_plot.addItem(center_dot)

    def reset(self):
        """Reset timer to initial state"""
        self.timer.stop()
        self.running = False
        self.start_pause.setText("▶️ Start")
        
        # Reset to default 25 minutes
        self.total_seconds = 25 * 60
        self.remaining = self.total_seconds
        self.linked_task_index = None
        self.start_time = None
        
        # Update display
        self.time_label.setText("25:00")
        self.time_label.setStyleSheet("color: #58a6ff; background: transparent;")
        self._draw_circular_progress(1.0)
        
        # Reset status
        self.status_label.setText("Ready to focus")
        self.status_label.setStyleSheet("color: #8b949e; font-size: 14px;")