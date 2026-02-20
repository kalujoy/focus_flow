import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tasks.json")

class TaskManager:
    def __init__(self):
        self.tasks = self._load()

    def _load(self):
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save(self):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2)

# def add_task(self, text, priority, due_date=None, timer_duration=25):
#     task = {
#         "text": text.strip(),
#         "priority": priority,
#         "due_date": due_date,
#         "timer_duration": timer_duration,           # ← new field
#         "done": False,
#         "created": datetime.now().isoformat(),
#         "completed_before_time": False,             # for wins
#         "completion_time_seconds": None             # for stats
#     }
#     self.tasks.append(task)
#     self.save()
#     return task

def add_task(self, text, priority, due_date=None, timer_duration=25):
    task = {
        "text": text.strip(),
        "priority": priority,
        "due_date": due_date,
        "timer_duration": timer_duration,  # NEW: default 25 minutes
        "done": False,
        "created": datetime.now().isoformat(),
        "completed_before_time": False,    # For win tracking
        "completion_time_seconds": None    # For stats
    }
    self.tasks.append(task)
    self.save()
    return task

    def mark_done(self, index, state=True):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = state
            self.save()

    def delete(self, index):    
        if 0 <= index < len(self.tasks):    
            del self.tasks[index]
            self.save()

    def get_completed_count_by_date(self):
        """For analytics: count completed tasks by date"""
        from collections import Counter
        dates = [datetime.fromisoformat(t["created"][:10]) for t in self.tasks if t["done"]]
        return Counter(d.date() for d in dates)