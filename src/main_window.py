import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QLineEdit, QComboBox, QFrame, QDateEdit, QMessageBox,
    QDialog, QFormLayout, QSpinBox, QDialogButtonBox, QTextEdit, QScrollArea,
    QGridLayout
)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFont, QColor, QIcon

from .task_manager import TaskManager
from .pomodoro_widget import PomodoroWidget
from .analytics_widget import AnalyticsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FocusFlow - Productivity Suite")
        self.resize(1280, 820)

        self.task_manager = TaskManager()
        self.pomodoro_widget = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("FocusFlow")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #58a6ff; margin-bottom: 10px;")
        main_layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #30363d; top: -1px; background: #0d1117; }
            QTabBar::tab { 
                background: #161b22; color: #8b949e; padding: 10px 20px; 
                border-top-left-radius: 6px; border-top-right-radius: 6px;
            }
            QTabBar::tab:selected { background: #0d1117; color: #58a6ff; border: 1px solid #30363d; border-bottom: none; }
        """)
        main_layout.addWidget(self.tabs)

        self._setup_tasks_tab()
        self._setup_pomodoro_tab()
        self._setup_analytics_tab()

    def _setup_tasks_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #0d1117; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Input form (kept exactly as you had it)
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; }
            QLabel { color: #c9d1d9; font-size: 14px; font-weight: bold; }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                background: #0d1117; color: #c9d1d9; border: 1px solid #30363d;
                border-radius: 6px; padding: 8px;
            }
            QPushButton { background: #238636; color: white; border: none; border-radius: 8px; padding: 12px; font-size: 15px; font-weight: bold; }
            QPushButton:hover { background: #2ea043; }
        """)
        input_layout = QVBoxLayout(input_frame)

        self.task_input = QLineEdit(placeholderText="What needs to be done?")
        self.task_input.setMinimumHeight(45)
        input_layout.addWidget(self.task_input)

        row1 = QHBoxLayout()
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Educational", "Financial", "Cooking", "Personal", "Work", "Health", "Shopping", "Other"])
        row1.addWidget(QLabel("Category:"))
        row1.addWidget(self.category_combo)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        row1.addWidget(QLabel("Priority:"))
        row1.addWidget(self.priority_combo)

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate.currentDate())
        row1.addWidget(QLabel("Due Date:"))
        row1.addWidget(self.due_date_edit)
        input_layout.addLayout(row1)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notes...")
        self.notes_edit.setFixedHeight(60)
        input_layout.addWidget(self.notes_edit)

        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self._add_task)
        input_layout.addWidget(add_btn)

        content_layout.addWidget(input_frame)

        self.tasks_layout = QVBoxLayout()
        self.tasks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tasks_layout.setSpacing(15)
        tasks_widget = QWidget()
        tasks_widget.setLayout(self.tasks_layout)
        content_layout.addWidget(tasks_widget)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        self._refresh_tasks()
        self.tabs.addTab(tab, "📋 Tasks")

    def _refresh_tasks(self):
        while self.tasks_layout.count():
            child = self.tasks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i, task in enumerate(self.task_manager.tasks):
            card = QFrame()
            card.setMinimumHeight(180)
            card.setStyleSheet(f"""
                QFrame {{
                    background: #21262d; border-radius: 12px;
                    border-left: 8px solid {self._get_priority_color(task['priority'])};
                }}
            """)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 15, 20, 15)
            card_layout.setSpacing(8)

            # Header: Category & Priority (your current nice header)
            header = QHBoxLayout()
            icon_path = f"assets/icons/{task['category'].lower()}.png"
            cat_icon = QLabel()
            if os.path.exists(icon_path):
                cat_icon.setPixmap(QIcon(icon_path).pixmap(28, 28))
            
            prio_tag = QLabel(task["priority"].upper())
            prio_tag.setStyleSheet(f"background: {self._get_priority_color(task['priority'])}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;")
            
            header.addWidget(cat_icon)
            header.addWidget(prio_tag)
            header.addStretch()
            card_layout.addLayout(header)

            # Task Title
            title_lbl = QLabel(task["text"])
            title_lbl.setWordWrap(True)
            title_lbl.setFont(QFont("Segoe UI", 15, QFont.Weight.DemiBold))
            if task["done"]:
                title_lbl.setStyleSheet("color: #8b949e; text-decoration: line-through;")
            else:
                title_lbl.setStyleSheet("color: #ffffff;")
            card_layout.addWidget(title_lbl)

            # Info Grid (your current grid layout)
            info_layout = QGridLayout()
            info_layout.setContentsMargins(0, 5, 0, 5)
            
            due_lbl = QLabel(f"📅 Due: {task.get('due_date', 'None')}")
            timer_lbl = QLabel(f"⏱️ Timer: {task.get('timer_duration', 25)}m")
            for lbl in [due_lbl, timer_lbl]:
                lbl.setStyleSheet("color: #8b949e; font-size: 12px;")
            
            info_layout.addWidget(due_lbl, 0, 0)
            info_layout.addWidget(timer_lbl, 0, 1)

            if task.get("notes"):
                notes_lbl = QLabel(f"📝 {task['notes'][:100]}{'...' if len(task['notes']) > 100 else ''}")
                notes_lbl.setStyleSheet("color: #8b949e; font-size: 12px;")
                info_layout.addWidget(notes_lbl, 1, 0, 1, 2)
            
            card_layout.addLayout(info_layout)

            # Footer: Status & Buttons (your current footer + NEW Start Timer)
            footer = QHBoxLayout()
            if task["done"]:
                status = QLabel("✓ Done")
                status.setStyleSheet("color: #3fb950; font-weight: bold; font-size: 14px;")
                footer.addWidget(status)
            footer.addStretch()

            btn_style = "QPushButton { background: #30363d; color: white; border-radius: 6px; padding: 6px 14px; font-size: 12px; } QPushButton:hover { background: #444c56; }"
            
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet(btn_style)
            edit_btn.clicked.connect(lambda _, idx=i: self._edit_task(idx))

            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet(btn_style + "QPushButton:hover { background: #da3633; }")
            del_btn.clicked.connect(lambda _, idx=i: self._delete_task(idx))

            mark_btn = QPushButton("Unmark" if task["done"] else "Mark Done")
            if not task["done"]:
                mark_btn.setStyleSheet("QPushButton { background: #238636; color: white; border-radius: 6px; padding: 6px 14px; font-weight: bold; } QPushButton:hover { background: #2ea043; }")
            else:
                mark_btn.setStyleSheet(btn_style)
            mark_btn.clicked.connect(lambda _, idx=i: self._toggle_done(idx))

            # NEW: Start Pomodoro Timer button (this was the missing piece)
            timer_btn = QPushButton("Start Timer")
            timer_btn.setStyleSheet("QPushButton { background: #1f6feb; color: white; border-radius: 6px; padding: 6px 14px; font-weight: bold; } QPushButton:hover { background: #388bfd; }")
            timer_btn.clicked.connect(lambda _, idx=i: self._start_timer_for_task(idx))

            footer.addWidget(edit_btn)
            footer.addWidget(del_btn)
            footer.addWidget(mark_btn)
            footer.addWidget(timer_btn)  # <--- now present on every card

            card_layout.addLayout(footer)

            self.tasks_layout.addWidget(card)

    def _get_priority_color(self, priority):
        return {"High": "#ff5252", "Medium": "#ffb300", "Low": "#4caf50"}.get(priority, "#757575")

    def _add_task(self):
        text = self.task_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Required", "Please enter a task description.")
            return
        due = self.due_date_edit.date().toString("yyyy-MM-dd")
        self.task_manager.add_task(
            text, self.priority_combo.currentText(), self.category_combo.currentText(), 
            due if due != QDate.currentDate().toString("yyyy-MM-dd") else None, 
            notes=self.notes_edit.toPlainText().strip()
        )
        self._refresh_tasks()
        self.task_input.clear()
        self.notes_edit.clear()

    def _toggle_done(self, index):
        task = self.task_manager.tasks[index]
        new_state = not task["done"]

        # WIN DETECTION - fully working when timer is linked
        if new_state and self.pomodoro_widget and self.pomodoro_widget.running:
            if hasattr(self.pomodoro_widget, 'linked_task_index') and self.pomodoro_widget.linked_task_index == index:
                time_taken = self.pomodoro_widget.total_seconds - self.pomodoro_widget.remaining
                task["completion_time_seconds"] = time_taken
                if self.pomodoro_widget.remaining > 0:
                    task["completed_before_time"] = True
                    QMessageBox.information(
                        self, "🎉 WIN!",
                        f"Task completed {self.pomodoro_widget.remaining}s early!\n"
                        f"Time taken: {time_taken//60}m {time_taken%60}s"
                    )
                else:
                    QMessageBox.information(self, "✅ Complete", "Task finished on time!")

        self.task_manager.mark_done(index, new_state)
        self._refresh_tasks()

    def _delete_task(self, index):
        if QMessageBox.question(self, "Delete", "Delete this task?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.task_manager.delete(index)
            self._refresh_tasks()

    def _edit_task(self, index):
        task = self.task_manager.tasks[index]
        dlg = EditTaskDialog(self, task)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            task.update({
                "text": dlg.task_input.text(),
                "category": dlg.category_combo.currentText(),
                "priority": dlg.priority_combo.currentText(),
                "due_date": dlg.due_date_edit.date().toString("yyyy-MM-dd") if dlg.due_date_edit.date() != QDate.currentDate() else None,
                "notes": dlg.notes_edit.toPlainText()
            })
            self.task_manager.save()
            self._refresh_tasks()

    def _start_timer_for_task(self, index):
            """Start Pomodoro timer linked to this task"""
            task = self.task_manager.tasks[index]

            dialog = TimerDurationDialog(self, task.get("timer_duration", 25))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                 minutes = dialog.get_minutes()
                 task["timer_duration"] = minutes
                 self.task_manager.save()

                 # Switch to Pomodoro tab
                 self.tabs.setCurrentIndex(1)

                 # ✅ FIXED: call the real method that exists
                 self.pomodoro_widget.start_with_duration(
                 minutes * 60,
                 linked_task_index=index
             )

    def _on_task_timer_finished(self, index):
         """Called when a task-linked timer finishes"""
         task = self.task_manager.tasks[index]

         if not task["done"]:
             self.task_manager.mark_done(index, True)

             QMessageBox.information(
            self,
            "🎉 Congratulations!",
            f"You completed:\n\n{task['text']}\n\nGreat job staying focused!"
        )

             self._refresh_tasks()

    def _setup_pomodoro_tab(self):
            self.pomodoro_widget = PomodoroWidget()
            self.pomodoro_widget.timer_finished.connect(self._on_task_timer_finished)
            self.tabs.addTab(self.pomodoro_widget, "⏳ Pomodoro")


    def _setup_analytics_tab(self):
        widget = AnalyticsWidget(self.task_manager)
        self.tabs.addTab(widget, "📊 Analytics")


# --- Dialogs (unchanged) ---

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

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_minutes(self):
        return self.minutes_spin.value()


class EditTaskDialog(QDialog):
    def __init__(self, parent, task):
        super().__init__(parent)
        self.setWindowTitle("Edit Task")
        self.setFixedWidth(400)
        layout = QFormLayout(self)
        self.task_input = QLineEdit(task["text"])
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Educational", "Financial", "Cooking", "Personal", "Work", "Health", "Shopping", "Other"])
        self.category_combo.setCurrentText(task["category"])
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentText(task["priority"])
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        if task.get("due_date"):
            y, m, d = map(int, task["due_date"].split('-'))
            self.due_date_edit.setDate(QDate(y, m, d))
        else:
            self.due_date_edit.setDate(QDate.currentDate())
        self.notes_edit = QTextEdit(task.get("notes", ""))
        
        layout.addRow("Task:", self.task_input)
        layout.addRow("Category:", self.category_combo)
        layout.addRow("Priority:", self.priority_combo)
        layout.addRow("Due Date:", self.due_date_edit)
        layout.addRow("Notes:", self.notes_edit)
        
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)
        
    def _on_task_timer_finished(self, index):
        """Called when a task-linked timer finishes"""
        task = self.task_manager.tasks[index]

        if not task["done"]:
                self.task_manager.mark_done(index, True)

                QMessageBox.information(
                 self,
                    "🎉 Congratulations!",
                    f"You completed:\n\n{task['text']}\n\nGreat job staying focused!"
                )

                self._refresh_tasks()
