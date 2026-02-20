# from PyQt6.QtWidgets import (
#     QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
#     QTabWidget, QLineEdit, QComboBox, QListWidget, QListWidgetItem,
#     QMenu, QDateEdit, QMessageBox
# )
# from PyQt6.QtCore import Qt, QTimer, QDate
# from PyQt6.QtGui import QFont, QColor

# from .task_manager import TaskManager
# from .pomodoro_widget import PomodoroWidget
# from .analytics_widget import AnalyticsWidget

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("FocusFlow - Productivity Suite")
#         self.resize(1280, 820)

#         self.task_manager = TaskManager()

#         central = QWidget()
#         self.setCentralWidget(central)
#         main_layout = QVBoxLayout(central)
#         main_layout.setContentsMargins(20, 20, 20, 20)

#         # Title
#         title = QLabel("FocusFlow")
#         title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         title.setStyleSheet("color: #58a6ff; margin-bottom: 10px;")
#         main_layout.addWidget(title)

#         # Tabs
#         self.tabs = QTabWidget()
#         main_layout.addWidget(self.tabs)

#         self._setup_tasks_tab()
#         self._setup_pomodoro_tab()
#         self._setup_analytics_tab()

#     def _setup_tasks_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout(tab)

#         # Input row
#         input_row = QHBoxLayout()
#         self.task_input = QLineEdit(placeholderText="What needs to be done?")
#         self.task_input.setMinimumHeight(48)
#         input_row.addWidget(self.task_input)

#         self.priority_combo = QComboBox()
#         self.priority_combo.addItems(["Low", "Medium", "High"])
#         self.priority_combo.setFixedWidth(140)
#         input_row.addWidget(self.priority_combo)

#         self.due_date_edit = QDateEdit()
#         self.due_date_edit.setCalendarPopup(True)
#         self.due_date_edit.setFixedWidth(160)
#         self.due_date_edit.setDate(QDate.currentDate())
#         input_row.addWidget(self.due_date_edit)

#         add_btn = QPushButton("Add Task")
#         add_btn.setFixedSize(140, 48)
#         add_btn.clicked.connect(self._add_task)
#         input_row.addWidget(add_btn)

#         layout.addLayout(input_row)

#         # Actions toolbar
#         actions = QHBoxLayout()
#         mark_btn = QPushButton("Mark Done")
#         mark_btn.clicked.connect(self._mark_selected_done)
#         actions.addWidget(mark_btn)

#         unmark_btn = QPushButton("Unmark")
#         unmark_btn.clicked.connect(self._unmark_selected)
#         actions.addWidget(unmark_btn)

#         delete_btn = QPushButton("Delete")
#         delete_btn.clicked.connect(self._delete_selected)
#         actions.addWidget(delete_btn)

#         actions.addStretch()
#         layout.addLayout(actions)

#         # Task list
#         self.task_list = QListWidget()
#         self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
#         self.task_list.customContextMenuRequested.connect(self._show_context_menu)
#         layout.addWidget(self.task_list)

#         self._refresh_tasks()
#         self.tabs.addTab(tab, "📋 Tasks")

#     def _add_task(self):
#         text = self.task_input.text().strip()
#         if not text:
#             QMessageBox.warning(self, "Input Required", "Please enter a task description.")
#             return

#         due = self.due_date_edit.date().toString("yyyy-MM-dd")
#         if self.due_date_edit.date() == QDate.currentDate():
#             due = None

#         self.task_manager.add_task(
#             text,
#             self.priority_combo.currentText(),
#             due
#         )
#         self._refresh_tasks()
#         self.task_input.clear()

#     def _refresh_tasks(self):
#         self.task_list.clear()
#         for i, task in enumerate(self.task_manager.tasks):
#             item = QListWidgetItem()
#             prefix = "✓ " if task["done"] else "⬜ "
#             due_str = f"  (due: {task['due_date']})" if task.get("due_date") else ""
#             item.setText(f"{prefix}{task['text']}{due_str}")

#             color = {"High": "#ff5252", "Medium": "#ffb300", "Low": "#4caf50"}.get(task["priority"], "#757575")
#             item.setForeground(QColor(color))

#             if task["done"]:
#                 font = item.font()
#                 font.setStrikeOut(True)
#                 item.setFont(font)
#                 item.setForeground(QColor("#757575"))

#             item.setData(Qt.ItemDataRole.UserRole, i)  # store index
#             self.task_list.addItem(item)

#     def _get_selected_index(self):
#         item = self.task_list.currentItem()
#         if item:
#             return item.data(Qt.ItemDataRole.UserRole)
#         return -1

#     def _mark_selected_done(self):
#         idx = self._get_selected_index()
#         if idx >= 0:
#             self.task_manager.mark_done(idx, True)
#             self._refresh_tasks()

#     def _unmark_selected(self):
#         idx = self._get_selected_index()
#         if idx >= 0:
#             self.task_manager.mark_done(idx, False)
#             self._refresh_tasks()

#     def _delete_selected(self):
#         idx = self._get_selected_index()
#         if idx >= 0:
#             self.task_manager.delete(idx)
#             self._refresh_tasks()

#     def _show_context_menu(self, pos):
#         item = self.task_list.itemAt(pos)
#         if not item:
#             return
#         idx = item.data(Qt.ItemDataRole.UserRole)
#         task = self.task_manager.tasks[idx]

#         menu = QMenu(self)
#         if task["done"]:
#             menu.addAction("Unmark as Done", lambda: self.task_manager.mark_done(idx, False))
#         else:
#             menu.addAction("Mark as Done", lambda: self.task_manager.mark_done(idx, True))
#         menu.addAction("Delete Task", lambda: self.task_manager.delete(idx))
#         menu.exec(self.task_list.viewport().mapToGlobal(pos))

#         self._refresh_tasks()  # refresh after any action

#     def _setup_pomodoro_tab(self):
#         widget = PomodoroWidget()
#         self.tabs.addTab(widget, "⏳ Pomodoro")

#     def _setup_analytics_tab(self):
#         widget = AnalyticsWidget(self.task_manager)
#         self.tabs.addTab(widget, "📊 Analytics")
        
#         from PyQt6.QtWidgets import QDialog, QFormLayout, QSpinBox, QDialogButtonBox

# class TimerDurationDialog(QDialog):
#     def __init__(self, parent=None, default_minutes=25):
#         super().__init__(parent)
#         self.setWindowTitle("Set Timer Duration")
#         self.setFixedSize(300, 150)

#         layout = QFormLayout(self)

#         self.minutes_spin = QSpinBox()
#         self.minutes_spin.setRange(1, 120)
#         self.minutes_spin.setValue(default_minutes)
#         layout.addRow("Minutes:", self.minutes_spin)

#         buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
#         buttons.accepted.connect(self.accept)
#         buttons.rejected.connect(self.reject)
#         layout.addRow(buttons)

#     def get_minutes(self):
#         return self.minutes_spin.value()


from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QMenu, QDateEdit, QMessageBox, QDialog, QFormLayout, QSpinBox, QDialogButtonBox
)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFont, QColor

from .task_manager import TaskManager
from .pomodoro_widget import PomodoroWidget
from .analytics_widget import AnalyticsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusFlow - Productivity Suite")
        self.resize(1280, 820)

        self.task_manager = TaskManager()
        # Store reference to pomodoro widget for task-timer linking
        self.pomodoro_widget = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("FocusFlow")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #58a6ff; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self._setup_tasks_tab()
        self._setup_pomodoro_tab()
        self._setup_analytics_tab()

    def _setup_tasks_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Input row
        input_row = QHBoxLayout()
        self.task_input = QLineEdit(placeholderText="What needs to be done?")
        self.task_input.setMinimumHeight(48)
        input_row.addWidget(self.task_input)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setFixedWidth(140)
        input_row.addWidget(self.priority_combo)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setFixedWidth(160)
        self.due_date_edit.setDate(QDate.currentDate())
        input_row.addWidget(self.due_date_edit)

        add_btn = QPushButton("Add Task")
        add_btn.setFixedSize(140, 48)
        add_btn.clicked.connect(self._add_task)
        input_row.addWidget(add_btn)

        layout.addLayout(input_row)

        # Actions toolbar - ADDED "Start Timer for Task" button
        actions = QHBoxLayout()
        mark_btn = QPushButton("Mark Done")
        mark_btn.clicked.connect(self._mark_selected_done)
        actions.addWidget(mark_btn)

        unmark_btn = QPushButton("Unmark")
        unmark_btn.clicked.connect(self._unmark_selected)
        actions.addWidget(unmark_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._delete_selected)
        actions.addWidget(delete_btn)

        actions.addStretch()

        # NEW: Start Timer for Task button
        start_timer_btn = QPushButton("⏱️ Start Timer for Task")
        start_timer_btn.setFixedSize(180, 40)
        start_timer_btn.clicked.connect(self._start_timer_for_selected_task)
        actions.addWidget(start_timer_btn)

        layout.addLayout(actions)

        # Task list
        self.task_list = QListWidget()
        self.task_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self._show_context_menu)
        layout.addWidget(self.task_list)

        self._refresh_tasks()
        self.tabs.addTab(tab, "📋 Tasks")

    def _add_task(self):
        text = self.task_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Required", "Please enter a task description.")
            return

        due = self.due_date_edit.date().toString("yyyy-MM-dd")
        if self.due_date_edit.date() == QDate.currentDate():
            due = None

        self.task_manager.add_task(
            text,
            self.priority_combo.currentText(),
            due
        )
        self._refresh_tasks()
        self.task_input.clear()

    def _refresh_tasks(self):
        self.task_list.clear()
        for i, task in enumerate(self.task_manager.tasks):
            item = QListWidgetItem()
            prefix = "✓ " if task["done"] else "⬜ "
            due_str = f"  (due: {task['due_date']})" if task.get("due_date") else ""
            timer_str = f"  [{task.get('timer_duration', 25)}m]" if task.get("timer_duration") else ""
            item.setText(f"{prefix}{task['text']}{due_str}{timer_str}")

            color = {"High": "#ff5252", "Medium": "#ffb300", "Low": "#4caf50"}.get(task["priority"], "#757575")
            item.setForeground(QColor(color))

            if task["done"]:
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor("#757575"))

            item.setData(Qt.ItemDataRole.UserRole, i)  # store index
            self.task_list.addItem(item)

    def _get_selected_index(self):
        item = self.task_list.currentItem()
        if item:
            return item.data(Qt.ItemDataRole.UserRole)
        return -1

    # def _mark_selected_done(self):
    #     idx = self._get_selected_index()
    #     if idx >= 0:
    #         self.task_manager.mark_done(idx, True)
    #         self._refresh_tasks()

def _mark_selected_done(self):
    idx = self._get_selected_index()
    if idx >= 0:
        # Check if pomodoro is running for this task
        if (self.pomodoro_widget and 
            self.pomodoro_widget.running and 
            self.pomodoro_widget.linked_task_index == idx):
            
            # Calculate time taken
            time_taken = self.pomodoro_widget.total_seconds - self.pomodoro_widget.remaining
            self.task_manager.tasks[idx]["completion_time_seconds"] = time_taken
            
            # Check for win (finished early)
            if self.pomodoro_widget.remaining > 0:
                self.task_manager.tasks[idx]["completed_before_time"] = True
                QMessageBox.information(
                    self, "🎉 WIN!", 
                    f"Task completed {self.pomodoro_widget.remaining}s early!\n"
                    f"Time taken: {time_taken//60}:{time_taken%60:02d}"
                )
                self.pomodoro_widget._trigger_win()
            else:
                QMessageBox.information(self, "✅ Complete", "Task finished on time!")
        
        self.task_manager.mark_done(idx, True)
        self._refresh_tasks()
        
    def _unmark_selected(self):
        idx = self._get_selected_index()
        if idx >= 0:
            self.task_manager.mark_done(idx, False)
            self._refresh_tasks()

    def _delete_selected(self):
        idx = self._get_selected_index()
        if idx >= 0:
            self.task_manager.delete(idx)
            self._refresh_tasks()

    def _show_context_menu(self, pos):
        item = self.task_list.itemAt(pos)
        if not item:
            return
        idx = item.data(Qt.ItemDataRole.UserRole)
        task = self.task_manager.tasks[idx]

        menu = QMenu(self)
        if task["done"]:
            menu.addAction("Unmark as Done", lambda: self.task_manager.mark_done(idx, False))
        else:
            menu.addAction("Mark as Done", lambda: self.task_manager.mark_done(idx, True))
        menu.addAction("Delete Task", lambda: self.task_manager.delete(idx))
        menu.exec(self.task_list.viewport().mapToGlobal(pos))

        self._refresh_tasks()  # refresh after any action

    # NEW: Start timer for selected task with custom duration dialog
    def _start_timer_for_selected_task(self):
        idx = self._get_selected_index()
        if idx < 0:
            QMessageBox.warning(self, "No Selection", "Please select a task first.")
            return

        task = self.task_manager.tasks[idx]
        default_duration = task.get("timer_duration", 25)

        # Show custom duration dialog
        dialog = TimerDurationDialog(self, default_duration)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            custom_minutes = dialog.get_minutes()
            # Save as new default duration for this task
            task["timer_duration"] = custom_minutes
            self.task_manager.save()  # persist the change
            
            # Switch to Pomodoro tab (index 1)
            self.tabs.setCurrentIndex(1)
            
            # Start pomodoro with task's custom duration (convert to seconds)
            self.pomodoro_widget.start_with_duration(
                custom_minutes * 60, 
                linked_task_index=idx
            )
        else:
           pass  # User cancelled - don't switch tabs

    def _setup_pomodoro_tab(self):
        self.pomodoro_widget = PomodoroWidget()  # Store reference for task linking
        self.tabs.addTab(self.pomodoro_widget, "⏳ Pomodoro")

    def _setup_analytics_tab(self):
        widget = AnalyticsWidget(self.task_manager)
        self.tabs.addTab(widget, "📊 Analytics")


# NEW: Custom timer duration dialog class (moved to proper location)
class TimerDurationDialog(QDialog):
    def __init__(self, parent=None, default_minutes=25):
        super().__init__(parent)
        self.setWindowTitle("Set Timer Duration")
        self.setFixedSize(320, 160)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        layout = QFormLayout(self)

        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(1, 120)
        self.minutes_spin.setValue(default_minutes)
        self.minutes_spin.setSuffix(" minutes")
        layout.addRow("Duration:", self.minutes_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_minutes(self):
        return self.minutes_spin.value()